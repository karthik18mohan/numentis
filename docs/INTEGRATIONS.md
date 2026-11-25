# Integrations: setup steps

Code for all of this is on branch `skills-lab-v2` and deploys with the site. Each piece switches on when its Vercel environment variables are set (Vercel > numentis-skills-lab > Settings > Environment Variables, tick Production and Preview, then redeploy). Until then the site works as before and the form says it is in preview.

Public review URL: https://numentis.vercel.app (and https://numentis-skills.vercel.app). Both follow `skills-lab-v2`.

## 0. Let the client open the site (one click, must be done by you)

Vercel > numentis-skills-lab > Settings > Deployment Protection > Vercel Authentication: off > Save.

## 1. Leads into a Google Sheet (all channels)

`/api/lead` receives the website form, WhatsApp handoffs and voice-agent bookings.

1. Create a Google Sheet. Row 1: `Time | Name | Mobile | You are | Language | Source | Medium | Campaign | Page`.
2. Extensions > Apps Script, paste `docs/google-sheet-lead-script.gs`, Save.
3. Deploy > New deployment > Web app. Execute as: Me. Who has access: Anyone. Authorise once. Copy the URL.
4. Vercel env: `SHEET_WEBHOOK_URL` = that URL. Redeploy.

## 2. WhatsApp AI assistant

Webhook: `https://numentis.vercel.app/api/whatsapp`. It answers from `docs/knowledge-base.md` using Gemini (free tier), says it is an AI, replies in English or Malayalam, and hands over to a human when asked (or when it cannot answer): the user is told a counsellor will reply, the counsellor gets a WhatsApp alert, and the lead goes to the sheet.

1. Gemini key: https://aistudio.google.com/apikey > Create API key. Vercel env `GEMINI_API_KEY`.
2. Meta app (developers.facebook.com > your app > WhatsApp > API Setup):
   - Copy the temporary access token > Vercel env `WA_TOKEN` (expires in 24 h; for longer, create a System User token in Business Settings with `whatsapp_business_messaging`).
   - Copy the Phone number ID > Vercel env `WA_PHONE_NUMBER_ID`.
   - Add your own phone (and the counsellor's) under "To" as test recipients. The free test number can only message these.
3. App settings > Basic > App secret > Vercel env `WA_APP_SECRET` (checks that webhook calls really come from Meta).
4. Make up any long random string > Vercel env `WA_VERIFY_TOKEN`. Redeploy.
5. WhatsApp > Configuration > Webhook: Callback URL `https://numentis.vercel.app/api/whatsapp`, Verify token = the same string > Verify and save. Then Manage > subscribe to `messages`.
6. Vercel env `COUNSELLOR_WHATSAPP` = counsellor's number with country code (receives handoff and new-lead alerts).
7. Test: from your phone, message the test number "What is the fee?", then "I want to talk to a counsellor".
8. Optional "Chat on WhatsApp" button on the site: set `WHATSAPP_NUMBER` in `tools/build_v2.py`, rebuild, QC, push.

Note: each message is answered on its own (no chat memory yet). Alerts to the counsellor only arrive if the counsellor has messaged the business number in the last 24 hours (a Meta rule); otherwise they still land in the sheet.

## 3. AI voice assistant (ElevenLabs, free plan: 15 minutes)

1. Sign up at elevenlabs.io. Developers > API keys > create a key.
2. In PowerShell, from the repo folder:
   ```
   $env:ELEVENLABS_API_KEY = "<key>"
   python tools/elevenlabs_agent.py
   python tools/build_v2.py
   python qc.py
   ```
   The script creates the agent (AI disclosure in its first line, knowledge base, a `book_counselling` tool that posts to `/api/lead`), allows the widget on the Numentis domains, and writes the agent id into `build_v2.py`. Re-running it updates the same agent.
3. Push. A "Talk to our AI assistant" button appears in the counselling section and the form. The ElevenLabs widget script loads only when someone clicks it.
4. Check in the ElevenLabs dashboard: the agent is public (no auth) and the voice sounds right. Malayalam is not confirmed on ElevenLabs; the agent runs in English (`$env:VOICE_LANGUAGE` to change).

Phone-number calling (a real number people dial) needs a paid telephony setup (Sarvam or Exotel/Twilio) and is not part of the free test.

## Local checks

```
python tools/serve.py        # http://127.0.0.1:8790 (8765 is used by another program on this PC)
python qc.py                 # brand QC, expect 47/47
python tools/t_book.py       # booking form flow
```
