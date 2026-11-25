import { KB } from './_kb.mjs';

const env = (k) => (process.env[k] || '').trim();
const GRAPH = 'https://graph.facebook.com/v21.0';

export const waReady = () => Boolean(env('WA_TOKEN') && env('WA_PHONE_NUMBER_ID'));

export async function waSend(to, text) {
  if (!waReady()) return false;
  const r = await fetch(`${GRAPH}/${env('WA_PHONE_NUMBER_ID')}/messages`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${env('WA_TOKEN')}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ messaging_product: 'whatsapp', to: String(to).replace(/\D/g, ''), type: 'text', text: { body: text.slice(0, 4000) } }),
  });
  if (!r.ok) console.error('whatsapp send failed', r.status, await r.text());
  return r.ok;
}

export async function waMarkRead(messageId) {
  if (!waReady()) return;
  await fetch(`${GRAPH}/${env('WA_PHONE_NUMBER_ID')}/messages`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${env('WA_TOKEN')}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ messaging_product: 'whatsapp', status: 'read', message_id: messageId }),
  }).catch(() => {});
}

async function toSheet(lead) {
  const url = env('SHEET_WEBHOOK_URL');
  if (!url) return false;
  const r = await fetch(url, { method: 'POST', headers: { 'Content-Type': 'text/plain;charset=utf-8' }, body: JSON.stringify(lead), redirect: 'follow' });
  if (!r.ok) console.error('sheet webhook failed', r.status);
  return r.ok;
}

export async function alertCounsellor(text) {
  const to = env('COUNSELLOR_WHATSAPP');
  return to ? waSend(to, text) : false;
}

export async function saveLead(lead) {
  const summary = [`New ${lead.source === 'whatsapp' ? 'WhatsApp' : lead.source === 'voice' ? 'voice' : 'website'} lead`, `${lead.name} ${lead.mobile}`, lead.who, lead.language && `Language: ${lead.language}`, lead.campaign && `Campaign: ${lead.campaign}`, lead.page].filter(Boolean).join('\n');
  const [sheet, alert] = await Promise.all([toSheet(lead).catch(() => false), alertCounsellor(summary).catch(() => false)]);
  console.log('lead', lead.source || 'website', { sheet, alert });
  return { sheet, alert };
}

export const HANDOFF = '[[HANDOFF]]';

export async function askAssistant(userText, userName) {
  const key = env('GEMINI_API_KEY');
  if (!key) return null;
  const model = env('GEMINI_MODEL') || 'gemini-2.5-flash';
  const system = `${KB}\n\n## Channel\nYou are replying on WhatsApp${userName ? ` to ${userName}` : ''}. Each message arrives without the earlier conversation, so do not refer to "earlier". If this looks like the first message (a greeting or a general question), start by saying you are the Numentis Skills Lab AI assistant. When you must hand over to a human counsellor, reply with a short line saying a counsellor will message them, and end the reply with ${HANDOFF}.`;
  const r = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'x-goog-api-key': key },
    body: JSON.stringify({
      systemInstruction: { parts: [{ text: system }] },
      contents: [{ role: 'user', parts: [{ text: userText.slice(0, 2000) }] }],
      generationConfig: { temperature: 0.3, maxOutputTokens: 800, thinkingConfig: { thinkingBudget: 0 } },
    }),
  });
  if (!r.ok) { console.error('gemini failed', r.status, await r.text()); return null; }
  const j = await r.json();
  const c = j.candidates?.[0];
  const text = (c?.content?.parts || []).map((p) => p.text || '').join('').trim();
  if (!text) console.error('gemini empty', c?.finishReason, JSON.stringify(j.promptFeedback || {}));
  return text || null;
}
