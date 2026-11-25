import { saveLead } from './_lib.mjs';

const clip = (v, n) => String(v ?? '').trim().slice(0, n);

export async function POST(request) {
  let d;
  try { d = await request.json(); } catch { return Response.json({ ok: false, error: 'bad_json' }, { status: 400 }); }
  const lead = {
    time: new Date().toISOString(),
    name: clip(d.name, 80),
    mobile: clip(d.mobile, 20),
    who: clip(d.who, 60),
    language: clip(d.language, 20),
    source: clip(d.source, 60),
    medium: clip(d.medium, 60),
    campaign: clip(d.campaign, 120),
    page: clip(d.page, 300),
  };
  if (lead.name.length < 2 || !/^[+0-9 ()-]{8,20}$/.test(lead.mobile) || d.consent !== 'yes') {
    return Response.json({ ok: false, error: 'invalid' }, { status: 400 });
  }
  const r = await saveLead(lead);
  return Response.json({ ok: true, delivered: r.sheet || r.alert });
}
