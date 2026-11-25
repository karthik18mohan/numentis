# Numentis Skills Lab website: handoff (for Cowork / Claude Code)

Owner: Karthik (freelance web developer; data scientist by day). Client: a new commerce and finance academy, brand **Numentis**. Everything below comes from one long session ending 25 Nov 2026. Branch of record: **`skills-lab-v2`** on GitHub `karthik18mohan/numentis`. **Never push to `main` until Karthik says so.**

## 1. Scope and standing rules
- Site for **Numentis Skills Lab only**: one programme, "Basic Level Accounts Executive". 4 months, 6 modules, in person in Calicut, fee ₹50,000 (₹40,000 if paid in full at once). Batch dates "will be announced soon".
- **Two pages only**: Home (`index.html`) and The programme (`programme.html`). Book counselling is a button/dialog on both, not a page.
- Follow the **Numentis Brand Manual (100-page PDF) 100%**. The client's folder `Numentis_Website_Preview` is the source of **facts and wording only**, never layout, design or visuals. The client's HTML uses extra fonts (Instrument Serif) not in the manual; do not copy that.
- Goal: "wow factor", Gen-Z appealing but professional, not childish. Minimal imagery (texture only, no people or stock photos).
- **Run the brand QC (`qc.py`) before every deploy** and report what passed.
- Workflow: new branch, Vercel preview, no push to main. Karthik reviews, then says when to merge.
- No dummy contact details. Phone/email/address are client gaps (due 30 Nov). Do not invent.
- Karthik often dictates by voice and is terse. He gives visual feedback by screenshot. Keep replies short and plain.
- Commit trailers used: `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>` and `Claude-Session: https://claude.ai/code/session_01YVtJxePtTa1fLJga4AdNRK`.
- A Stop hook repeatedly claims "N unpushed commits, no remote branch". It is a false alarm: verify with `git ls-remote origin skills-lab-v2` vs `git rev-parse HEAD` (they have been identical every time).

## 2. Brand system as implemented
- Palette only: terracotta `#C2410C`, ink `#0F1419`, paper `#FAFAF7`, cream `#F5F1EA`, mute `#6B6F76` (plus alpha tints). Terracotta only for CTA buttons, the italic heading keyword and accent rules; never a dot/bullet/circle; never gradient. Dark (Atelier Dark) only for hero and footer.
- Fonts, self-hosted woff2 in `assets/fonts/` (no Google Fonts requests): **Fraunces** (headings 400, line-height 1.05, tracking -0.03em or tighter, opsz 144; italic only for emphasis words and the tagline), **Onest** (body), **JetBrains Mono** (labels, uppercase, .18em, numerics). Familjen Grotesk exists only inside the logo SVGs (outlined paths; logos are unmodified official files).
- ₹ is not in Onest or JetBrains Mono, so it is wrapped in `<span class="rs">` (Fraunces, via a `fraunces-rupee.woff2` subset). Arrows are inline SVG (no brand font has →).
- Tagline "Where numbers *think.*": Fraunces italic, last word terracotta (manual 01.3 and the colour rules). Position statement used verbatim.
- Voice rules: no jargon (synergy, leverage, journey...), no exclamation marks, no emoji, Indian number grouping.
- **Deliberate deviations from the manual's web spec, requested by Karthik**: body 16px (manual 15px), labels 12px (manual 11px), whole layout scaled to ~72% (his "zoom out to 70% and increase font"). `qc.py` is updated to expect these.

## 3. Design and interaction
- Hero (dark): a **ruled-notebook background** with pitch `--rl` (about 44px at 1440 wide). Text sits on the lines: eyebrow, the two H1 lines, the lead paragraph and the note. Each is offset about 2px above its line using calibrated `--bo1..4` variables. The H1 is 3 rulers tall (`--hf:3`). The two CTA buttons are 50px tall and are deliberately NOT tied to the ruler. A **tool ticker** (TallyPrime, Zoho Books, ERP, Excel, Power BI, GST, TDS, Payroll, PF, ESI) is pinned absolutely to the bottom of the first screen. Below 700px the grid collapses (`--rl:26px`, hero height auto, ticker static).
- `tools/base.py W H` measures how far each hero text baseline is from its ruled line at a given viewport (targets: line k at k*rl-1; expected error about -2px). Run it after any hero change.
- Sections: "The gap" (word-by-word scroll-lit paragraph; now completes once its bottom reaches about 70-75% of the viewport), position statement, six tasks with scroll-spy (JV, BRS, GST, TDS, PAY, MEC with tools), stats, "If you studied commerce, start here.", "Three steps to a seat.", booking section, footer (stacked white logo, tagline, alphabetical verticals list). Programme page: six modules, how we teach, career readiness (with the "we do not promise placement, interviews or salaries" note), fees, four FAQs.
- JS: IntersectionObserver reveals, count-up (₹ wrapped), sticky stacked cards (CSS), native `<dialog id="counsel">` form, `prefers-reduced-motion` honoured. Hero buttons are visible immediately (no entrance delay) because of ad traffic.

## 4. Code layout
- Repo root: `index.html`, `programme.html` (GENERATED), `vercel.json` (`cleanUrls` plus rewrite `/book` -> `/index.html`), `assets/site.css`, `assets/site.js`, fonts and logos, `qc.py`, `BRAND-CHECKLIST.md`, `docs/google-sheet-lead-script.gs`, `tools/`.
- **HTML is generated by `tools/build_v2.py`** (Python f-strings; data lists for tasks, modules, FAQ). Edit the builder, not the generated HTML. It writes to `OUT=/home/claude/numentis-v2`: change that path (or copy the output into the repo root) in a new environment. `qc.py` has hard-coded `SITE=/home/claude/numentis-v2` and `PACK=/mnt/user-data/uploads/Numentis_Brand_Final/Numentis_Brand_Final` (the client's brand pack with `Logo_Production/`, `Vertical_Lockups/` and `Numentis_Brand_Manual.pdf`). Adjust both. CSS/JS are hand-edited directly in `assets/`.
- Local serving for QC: `tools/serve.py` serves on `127.0.0.1:8765` with clean-URL handling. `qc.py` expects it running. Playwright and Chromium are used (fonts load locally).
- QC: `python3 qc.py` currently **47/47 pass**. It covers logo byte-equality with the pack, palette only, no gradients or circles, fonts self-hosted, banned words, no exclamation marks or emoji, position statement verbatim, facts present, no invented contact details, type specs, tagline italics, CTA colour, logo widths, no overflow at 360/390/768/1024/1440, no console errors, AA contrast, dialog open/Esc, link resolution. `tools/fontcheck.py` uses CDP to confirm no system-fallback glyphs.

## 5. Deployment
- Vercel project `numentis-skills-lab` (id `prj_gAOVVCnFEwNuukJAy3ZF16hkFAKR`, team `team_VY4eaWLL4pNvkDdF516A7NPI`, slug `karthik18mohan-1136s-projects`), Git-integrated: a push to a branch builds a preview, a push to `main` builds production. **`main` still holds the older one-page version and has not been touched.**
- Review URL for the client: **`https://numentis-skills.vercel.app`**, assigned to branch `skills-lab-v2`. `numentis.vercel.app` was requested but is taken by another account.
- **Open blocker**: the project has Vercel Authentication on (`all_except_custom_domains`), so visitors see a Vercel login. An attempt to turn it off from the agent was blocked by the environment. **Karthik must disable it himself**: Vercel > numentis-skills-lab > Settings > Deployment Protection > Vercel Authentication off > Save. Then the client can open the URL.
- The `/book` rewrite was only verified locally via `?book` (a deploy was queued at the last check). Verify `/book` on the live URL once public.
- Client's eventual domain is `numentis.in` (DNS to be added through Vercel Domains later, if wanted).

## 6. Ads and the lead form
- Ad link plan: `https://<site>/book?utm_source=meta&utm_campaign=...`. `/book`, `?book` and `#book` open the counselling form straight away over the landing page; the page loads behind it. `utm_source/medium/campaign` are saved with each lead.
- Performance (measured on throttled mobile): about 330-380 KB first load, first paint 1.1 s on a 4G profile and 1.8 s on a slow-3G profile, no third-party scripts, the form opens with no network request.
- The form (`<form data-endpoint="">` in the dialog) posts JSON to `data-endpoint` if set; empty = preview mode ("nothing was sent"). **To go live**: create a Google Sheet with header row `Time | Name | Mobile | You are | Language | Source | Medium | Campaign | Page`, paste `docs/google-sheet-lead-script.gs` into Extensions > Apps Script, deploy as Web app (Execute as Me, access Anyone), put the URL into `data-endpoint` in `tools/build_v2.py`'s `DIALOG`, rebuild, QC, push. Karthik must authorise the script once. The form uses `no-cors` POST so it cannot read the response.
- Later: instant counsellor alert (WhatsApp/email) on each lead.

## 7. Client's bigger asks (research done, nothing built yet)
1. **Traffic worry**: answered above (no delay from animations; the form is in-page).
2. **AI telecaller**: a Call button where an AI agent answers from a knowledge base, talks like a human, and hands over to a human agent if it can't answer. **Same for WhatsApp chat.**
   - Feasible. Disclose that it is an AI at the start of calls. Calls need a KYC'd Indian number (days) and do-not-disturb scrubbing for outbound. WhatsApp needs a verified Meta business account.
   - **Voice prices** (India): Sarvam managed voice agents ₹3.50/min pay-as-you-go down to ₹3.00 at volume, models included, **Malayalam supported** (11 Indian languages, code-mixed speech), plus telephony: Sarvam's own ₹0.20 per 30s pulse (₹0.40/min), number ₹59 per 30 days, forwarding to a phone ₹0.40 per pulse, unanswered calls not charged, bring-your-own Exotel/Twilio is free from Sarvam's side. Bolna about ₹5.5/min (pilot plan 12,000 min at $0.06; Malayalam not confirmed). Edesy ₹4-6/min. Vapi/Retell about $0.09-0.15/min (roughly ₹8-14; US-first). ElevenLabs Agents $0.08/min platform plus LLM plus telephony at cost; free plan 15 min; Malayalam not confirmed. Human call centre ₹7-8/min. Sources were vendor pages and a vendor-biased blog (Edesy): re-verify before quoting to the client.
   - **WhatsApp**: Meta per-message pricing; from 1 Oct 2026 each number gets 1,000 free service messages/month, then billed. Click-to-WhatsApp ad conversations free for up to 7 days. India rates cited: marketing about ₹0.86, utility/authentication about ₹0.115. Provider (BSP) fees about ₹999-9,999/month or ₹0.10-0.30 per message, plus 18% GST.
   - **Free testing path**: Meta Cloud API developer app with the free test number (limited to a few pre-registered recipients, believed about 5, unconfirmed), a small webhook function on Vercel (`api/whatsapp`), and a free-tier LLM (Gemini or Groq; limits change). For voice: LiveKit Agents with the Sarvam plugin (`pip install "livekit-agents[sarvam]"`; talk via laptop mic with `python agent.py console`), ElevenLabs free 15 min, Bolna $5 credit. A real phone number cannot be tested for free.
   - **Build vs buy**: self-hosting models needs about $0.44/hr per L4 GPU (about ₹30k/month) and only beats APIs above roughly 50,000-130,000 min/month; this client will be nearer 5,000 min/month. Do not self-host. Recommendation: Karthik owns the website, form, WhatsApp function and lead tracking, and uses Sarvam as the managed voice engine under his own brand (so the client does not need an AI agency); move to his own LiveKit build once volume justifies it.
   - **Suggested pricing (Karthik's margin, my judgment, not market data)**: proof of concept ₹40-60k, production build ₹1.5-3 lakh, retainer ₹15-25k/month, usage resold at about ₹5.5-6/min against about ₹4/min cost (about ₹7k/month margin at 4,500 min); WhatsApp fees passed through plus 15-20%. Estimated effort: proof of concept 25-40 hours, production 100-150 hours.
   - Karthik said he has already created a **Meta developer account and connectors in a different Cowork/Claude Code chat**, and wants the WhatsApp assistant and the Google Sheet created automatically there. Connections do not carry across sessions, so this work belongs in the session that has those connectors. Meta approval/login and the one-time Google script authorisation need Karthik himself.

## 8. Open items, in order
1. Karthik disables Vercel Authentication so the client can review `numentis-skills.vercel.app`.
2. Gather the client's corrections on content (they will verify the second builds).
3. Get contact details (phone, email, address) from the client; add via `build_v2.py`, rebuild, QC.
4. Create the lead Sheet, deploy the Apps Script, set `data-endpoint`, test end to end.
5. Build the WhatsApp assistant proof of concept (Vercel function, knowledge base from the site copy, human handoff flag), then the voice proof of concept on Sarvam.
6. Optional: custom domain `numentis.in`, ad pixel, remove any remaining preview wording once the form is live.
7. Merge `skills-lab-v2` to `main` only when Karthik says so.

## 9. Update 25 Nov 2026 (Windows session)

- Paths in `build_v2.py`, `qc.py`, `serve.py` are now relative to the repo; the brand pack is found at `../Numentis_Brand_Final` (override with `NUMENTIS_PACK`). Local server port is 8790 (`NUMENTIS_PORT`), as 8765 is taken on Karthik's PC. `.gitattributes` keeps LF so logo SVGs stay byte-identical on Windows.
- `numentis.vercel.app` is now attached to project `numentis-skills-lab`, following branch `skills-lab-v2`.
- Built: `/api/lead` (one lead endpoint for form, WhatsApp and voice; forwards to the Sheet and alerts the counsellor), `/api/whatsapp` (Meta Cloud API webhook + Gemini answers + human handoff), `tools/elevenlabs_agent.py` (voice agent + booking tool), optional "Talk to our AI assistant" and "Chat on WhatsApp" buttons. Knowledge base: `docs/knowledge-base.md` (builder copies it to `api/_kb.mjs`).
- Everything switches on through Vercel env vars; steps in `docs/INTEGRATIONS.md`. Vercel Authentication still needs Karthik to switch it off.

## 10. Two review sites (25 Nov 2026, evening)

| Site | Branch | What it shows |
|---|---|---|
| numentis.vercel.app (also numentis-skills.vercel.app) | `skills-lab-v2` | Client review site. No WhatsApp or call features: `CONTACT_FEATURES=False` in `tools/build_v2.py`. |
| numentis1.vercel.app | `skills-lab-v2-ai` | Same site plus floating WhatsApp and call circles: `CONTACT_FEATURES=True`. |

- The two branches differ only in that one line and the generated HTML. Make changes on `skills-lab-v2`, then bring them to `skills-lab-v2-ai` (cherry-pick, or merge and keep `CONTACT_FEATURES=True`), rebuild there, QC, push.
- Both branches keep the APIs (`/api/lead`, `/api/whatsapp`). The Meta webhook and the ElevenLabs booking tool point at `numentis.vercel.app`, so they keep working.
- WhatsApp circle: `wa.me/15551847712?text=Hi` (Meta test number). Replace `WHATSAPP_NUMBER` with the real Numentis number once it is registered in Meta.
- WhatsApp bot: Meta delivers messages (WABA 1453085660373335 linked to the app with `tools/wa_subscribe.ps1`), but replies fail with 131031 "Business account locked" until Numentis completes Meta business verification. Gemini default model `gemini-3.8-flash`, with fallbacks to other flash models when busy.
- Call circle: one click starts a call with ElevenLabs agent `agent_4501m89wekzhe6ys4kedff6spmjn` (Karthik's ElevenLabs account, free plan, 15 min a month, no commercial licence; Starter or higher before launch). The agent was set up in the ElevenLabs dashboard: knowledge base prompt, English and Malayalam, `book_counselling` tool to `/api/lead`, allowlist numentis.vercel.app, numentis1.vercel.app, numentis-skills.vercel.app, numentis.in, www.numentis.in.
- Before launch: Vercel Pro (Hobby is non-commercial), ElevenLabs Starter or higher, Gemini paid tier (free Flash is about 20 requests a day), Meta business verification.
