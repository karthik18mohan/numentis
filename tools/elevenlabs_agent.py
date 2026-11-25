"""Create or update the Numentis Skills Lab voice agent on ElevenLabs.

Usage (PowerShell):
  $env:ELEVENLABS_API_KEY = "<your key>"
  python tools/elevenlabs_agent.py [site_url]

site_url defaults to https://numentis.vercel.app. The agent id is saved in tools/elevenlabs_agent.json and
written into VOICE_AGENT_ID in tools/build_v2.py; rebuild afterwards.
"""
import json, os, pathlib, re, sys, urllib.request, urllib.error

ROOT = pathlib.Path(__file__).resolve().parent.parent
STATE = ROOT / 'tools' / 'elevenlabs_agent.json'
API = 'https://api.elevenlabs.io/v1/convai'
KEY = os.environ.get('ELEVENLABS_API_KEY', '').strip()
SITE = (sys.argv[1] if len(sys.argv) > 1 else 'https://numentis.vercel.app').rstrip('/')
LANG = os.environ.get('VOICE_LANGUAGE', 'en')
LLM = os.environ.get('VOICE_LLM', 'gemini-2.5-flash')

FIRST = ('Hello, I am the Numentis Skills Lab AI assistant. I can answer questions about the '
         'Accounts Executive programme or book a counselling call for you. How can I help?')
VOICE_RULES = '''
## Channel: voice call on the website
- Speak naturally, in short sentences. Say amounts in words, for example "fifty thousand rupees".
- To book counselling: ask for the caller's name and mobile number, read the number back to confirm it, ask whether
  Numentis may contact them by phone or WhatsApp, and only after a yes call the book_counselling tool.
- If the caller wants a human, or you cannot answer, offer to book counselling so a counsellor calls them back.
- After the tool succeeds, tell the caller a counsellor will call or WhatsApp them shortly.
'''


def call(method, path, body=None):
    req = urllib.request.Request(API + path, method=method, data=json.dumps(body).encode() if body is not None else None,
                                 headers={'xi-api-key': KEY, 'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read() or b'{}')
    except urllib.error.HTTPError as e:
        raise RuntimeError(f'{method} {path} -> {e.code}: {e.read().decode(errors="replace")[:600]}')


def tool_config():
    prop = lambda d: {'type': 'string', 'description': d}
    return {'tool_config': {
        'type': 'webhook',
        'name': 'book_counselling',
        'description': 'Book a counselling call. Use only after the caller has given a name, a confirmed mobile number and agreed to be contacted.',
        'api_schema': {
            'url': f'{SITE}/api/lead',
            'method': 'POST',
            'request_body_schema': {
                'type': 'object',
                'description': 'Counselling request from a voice call',
                'properties': {
                    'name': prop("Caller's name"),
                    'mobile': prop("Caller's mobile number with country code, digits and + only, for example +919800000000"),
                    'language': prop('English or Malayalam, whichever the caller prefers'),
                    'who': prop('One line about the caller, for example final-year B.Com student, or parent'),
                    'consent': prop('The word yes, only after the caller agrees to be contacted'),
                    'source': prop('Always the word voice'),
                },
                'required': ['name', 'mobile', 'consent', 'source'],
            },
        },
    }}


def main():
    if not KEY:
        sys.exit('Set ELEVENLABS_API_KEY first (ElevenLabs > Developers > API keys).')
    state = json.loads(STATE.read_text()) if STATE.exists() else {}
    kb = (ROOT / 'docs' / 'knowledge-base.md').read_text(encoding='utf-8')

    tool_ids = []
    try:
        if state.get('tool_id'):
            call('PATCH', f"/tools/{state['tool_id']}", tool_config())
        else:
            state['tool_id'] = call('POST', '/tools', tool_config())['id']
        tool_ids = [state['tool_id']]
        print('booking tool ready')
    except Exception as e:
        print('WARNING: could not set up the booking tool, the agent will work without it.\n ', e)

    cfg = {
        'name': 'Numentis Skills Lab assistant',
        'conversation_config': {
            'agent': {'first_message': FIRST, 'language': LANG,
                      'prompt': {'prompt': kb + VOICE_RULES, 'llm': LLM, 'tool_ids': tool_ids}},
        },
    }
    if state.get('agent_id'):
        call('PATCH', f"/agents/{state['agent_id']}", cfg)
        print('agent updated')
    else:
        state['agent_id'] = call('POST', '/agents/create', cfg)['agent_id']
        print('agent created')
    STATE.write_text(json.dumps(state, indent=2))

    host = re.sub(r'^https?://', '', SITE)
    try:
        call('PATCH', f"/agents/{state['agent_id']}", {'platform_settings': {'auth': {'enable_auth': False, 'allowlist': [
            {'hostname': h} for h in sorted({host, 'numentis.vercel.app', 'numentis-skills.vercel.app', 'numentis.in', 'www.numentis.in', 'localhost'})]}}})
        print('website widget allowed on', host)
    except Exception as e:
        print('WARNING: set the domain allowlist by hand (agent > Security/Advanced).\n ', e)

    b = ROOT / 'tools' / 'build_v2.py'
    src = b.read_text(encoding='utf-8')
    b.write_text(re.sub(r"^VOICE_AGENT_ID='[^']*'", f"VOICE_AGENT_ID='{state['agent_id']}'", src, flags=re.M), encoding='utf-8', newline='\n')
    print('agent id', state['agent_id'], 'saved in tools/build_v2.py. Now run: python tools/build_v2.py')


if __name__ == '__main__':
    main()
