import crypto from 'node:crypto';
import { askAssistant, waSend, waMarkRead, saveLead, HANDOFF } from './_lib.mjs';

const env = (k) => (process.env[k] || '').trim();
const HUMAN = /\b(human|person|agent|counsell?or|call me|talk to (someone|somebody)|manager)\b/i;
const FALLBACK = 'Thank you for your message. A Numentis Skills Lab counsellor will reply to you here shortly.';
const HANDED = 'I have passed this to a Numentis Skills Lab counsellor. They will message you here shortly.';

export function GET(request) {
  const q = new URL(request.url).searchParams;
  if (q.get('hub.mode') === 'subscribe' && env('WA_VERIFY_TOKEN') && q.get('hub.verify_token') === env('WA_VERIFY_TOKEN')) {
    return new Response(q.get('hub.challenge') || '', { status: 200 });
  }
  return new Response('forbidden', { status: 403 });
}

function signatureOk(raw, header) {
  const secret = env('WA_APP_SECRET');
  if (!secret) return true;
  if (!header?.startsWith('sha256=')) return false;
  const want = crypto.createHmac('sha256', secret).update(raw).digest('hex');
  const got = header.slice(7);
  return got.length === want.length && crypto.timingSafeEqual(Buffer.from(got), Buffer.from(want));
}

async function handle(msg, name) {
  const from = msg.from;
  await waMarkRead(msg.id);
  if (msg.type !== 'text') {
    await waSend(from, 'I can read text messages only. Please type your question, in English or Malayalam.');
    return;
  }
  const text = msg.text?.body || '';
  let reply = HUMAN.test(text) ? `${HANDED} ${HANDOFF}` : await askAssistant(text, name).catch(() => null);
  if (!reply) reply = `${FALLBACK} ${HANDOFF}`;
  const handoff = reply.includes(HANDOFF);
  reply = reply.replaceAll(HANDOFF, '').trim();
  await waSend(from, reply);
  if (handoff) {
    await saveLead({ time: new Date().toISOString(), name: name || 'WhatsApp contact', mobile: `+${from}`, who: 'WhatsApp chat: needs a counsellor', language: '', source: 'whatsapp', medium: 'chat', campaign: '', page: `Last message: ${text.slice(0, 250)}` });
  }
}

export async function POST(request) {
  const raw = await request.text();
  if (!signatureOk(raw, request.headers.get('x-hub-signature-256'))) return new Response('bad signature', { status: 401 });
  let body;
  try { body = JSON.parse(raw); } catch { return new Response('ok'); }
  const jobs = [];
  for (const entry of body.entry || []) {
    for (const change of entry.changes || []) {
      const v = change.value || {};
      const names = Object.fromEntries((v.contacts || []).map((c) => [c.wa_id, c.profile?.name || '']));
      for (const msg of v.messages || []) jobs.push(handle(msg, names[msg.from]).catch((e) => console.error('whatsapp handle', e)));
    }
  }
  await Promise.all(jobs);
  return new Response('ok');
}
