import pathlib,json
OUT=pathlib.Path(__file__).resolve().parent.parent
VOICE_AGENT_ID=''   # ElevenLabs agent id (printed by tools/elevenlabs_agent.py); empty hides the voice button
WHATSAPP_NUMBER=''  # WhatsApp business number, digits only with country code (e.g. 91XXXXXXXXXX); empty hides the link
FONTS="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..600;1,9..144,300..600&family=JetBrains+Mono:wght@400;500&family=Onest:wght@300..600&display=swap"

def head(title,desc,page):
    return f'''<!doctype html>
<html lang="en" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#FAFAF7">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="preload" href="/assets/fonts/fraunces-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/onest.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/site.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="progress" aria-hidden="true"></div>
{header(page)}
'''

def header(page):
    cur=lambda k:' aria-current="page"' if k==page else ''
    return f'''<header class="head">
  <div class="wrap">
    <a class="brand" href="/" aria-label="Numentis Skills Lab, home"><img src="/assets/logo-skills-lab-horizontal-ink.svg" width="226" height="52" alt="Numentis Skills Lab"></a>
    <nav class="nav" aria-label="Main">
      <a href="/"{cur('home')}>Home</a>
      <a href="/programme"{cur('programme')}>The programme</a>
      <a href="/#admissions">Admissions</a>
      <a href="/programme#questions">Questions</a>
      <a class="btn btn--primary" href="#" data-counsel>Book counselling</a>
    </nav>
    <button class="burger" id="menuOpen" aria-label="Open menu" aria-expanded="false" aria-controls="menu"><i></i></button>
  </div>
</header>
<div class="menu dark" id="menu" aria-hidden="true">
  <div class="menu__top"><img src="/assets/logo-skills-lab-horizontal-white.svg" width="192" height="44" alt="Numentis Skills Lab"><button class="menu__x" id="menuX" aria-label="Close menu">&times;</button></div>
  <nav aria-label="Mobile">
    <a href="/">Home</a>
    <a href="/programme">The programme</a>
    <a href="/#admissions">Admissions</a>
    <a href="/programme#questions">Questions</a>
  </nav>
  <a class="btn btn--primary" href="#" data-counsel>Book counselling</a>
</div>
'''

DIALOG='''<dialog id="counsel" aria-labelledby="dlgT">
  <div class="dlg">
    <form novalidate data-endpoint="/api/lead">
      <div class="dlg__top"><div><p class="label">Counselling</p><h2 id="dlgT">Book a counselling <em>session.</em></h2></div><button type="button" class="x" data-close aria-label="Close">&times;</button></div>
      <p class="s">Leave your number and a counsellor will call or WhatsApp you, in English or Malayalam.</p>
      <div class="field"><label class="label" for="fullname">Your name</label><input id="fullname" name="fullname" autocomplete="name" required></div>
      <div class="field"><label class="label" for="mobile">Mobile number (WhatsApp)</label><input id="mobile" name="mobile" type="tel" inputmode="tel" autocomplete="tel" placeholder="+91" required></div>
      <div class="field"><label class="label" for="who">You are</label><select id="who" name="who" required><option value="">Choose one</option><option>Final-year student</option><option>Graduate, looking for work</option><option>Working in accounts</option><option>Parent or guardian</option><option>Other</option></select></div>
      <div class="field"><label class="label" for="lang">Talk to me in</label><select id="lang" name="lang"><option>English</option><option>Malayalam</option></select></div>
      <div class="field field--c"><input type="checkbox" id="consent" name="consent"><label for="consent">I agree that Numentis may contact me about this enquiry by phone, WhatsApp or email.</label></div>
      <p class="err" role="alert"></p>
      <button class="btn btn--primary" type="submit">Book counselling</button>
    </form>
    {TALK}
    <div class="done" hidden>
      <div class="dlg__top"><div><p class="label">Counselling</p><h2>Thank you.</h2></div><button type="button" class="x" data-close aria-label="Close">&times;</button></div>
      <p class="s">Preview: this form is not yet connected to the lead system, so nothing was sent.</p>
    </div>
  </div>
</dialog>
'''

def talk():
    b=[]
    if VOICE_AGENT_ID:b.append(f'<button type="button" class="btn btn--line" data-voice="{VOICE_AGENT_ID}">Talk to our AI assistant</button>')
    if WHATSAPP_NUMBER:b.append(f'<a class="btn btn--line" href="https://wa.me/{WHATSAPP_NUMBER}?text=Hello%2C%20I%20would%20like%20to%20know%20about%20the%20Accounts%20Executive%20programme." target="_blank" rel="noopener">Chat on WhatsApp</a>')
    return f'<div class="talk">{"".join(b)}</div>' if b else ''
DIALOG=DIALOG.replace('{TALK}',talk())

def footer():
    return '''<footer class="foot">
  <div class="wrap">
    <div class="foot__grid">
      <div class="foot__brand">
        <img src="/assets/logo-skills-lab-stacked-white.svg" width="220" height="116" alt="Numentis Skills Lab">
        <p class="tag">Where numbers <em>think.</em></p>
        <p class="about">A finance-led group for audit, strategy, technology and practical finance training.</p>
      </div>
      <div class="foot__biz">
        <p class="label" style="margin-bottom:8px">Businesses</p>
        <ul><li>Audit &amp; Advisory</li><li>Next</li><li>Skills Lab</li><li>Strategy &amp; Finance</li></ul>
      </div>
    </div>
    <div class="foot__base"><p class="label">&copy; 2026 Numentis Group</p><p class="label">numentis.in</p></div>
  </div>
</footer>
'''

def cta():
    return '''<section class="sec sec--cream cta">
  <div class="wrap cta__grid">
    <div data-r><p class="label">Counselling</p><h2>Book a counselling <em>session.</em></h2></div>
    <div data-r style="--d:1"><p class="lead">Leave your number and a counsellor will call or WhatsApp you, in English or Malayalam.</p><a class="btn btn--primary" href="#" data-counsel>Book counselling <span class="arr" aria-hidden="true"><svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M2 8h11M9 4l4 4-4 4"/></svg></span></a>'''+talk()+'''</div>
  </div>
</section>
'''

SCRIPT='<script src="/assets/site.js" defer></script>\n</body>\n</html>\n'

TASKS=[('JV','Post sales and purchase entries','TallyPrime'),('BRS','Reconcile the bank statement','Excel'),('GST','Prepare the GST return','Supervised'),('TDS','Work out TDS and file it','Supervised'),('PAY','Run payroll with PF and ESI','Payroll'),('MEC','Close the month and report','Power BI')]
TOOLS=['TallyPrime','Zoho Books','ERP','Excel','Power BI','GST','TDS','Payroll','PF','ESI']
tick=''.join(f'<span>{t}</span>' for t in TOOLS*2)

def stats(cls=''):
    return '''<div class="stats">
      <div><p class="label">Duration</p><span class="metric" data-count="4" data-suf=" months">4 months</span></div>
      <div><p class="label">Modules</p><span class="metric" data-count="6">6</span></div>
      <div><p class="label">Format</p><span class="metric sm">In person, Calicut</span></div>
      <div><p class="label">Fee</p><span class="metric" data-count="50000" data-pre="₹">₹50,000</span></div>
    </div>'''

home=head('Numentis Skills Lab | From degree to desk.','Practical accounts training for commerce graduates. Four months of the work an accounts office expects from day one. In person in Calicut.','home')
home+=f'''<main id="main">
<section class="hero dark">
  <div class="hero__ruled"></div><div class="hero__lit"></div><div class="hero__grain"></div>
  <div class="wrap">
    <div class="hero__eyebrow" data-in="1"><p class="label">Numentis Skills Lab</p><p class="label">Calicut</p></div>
    <h1 aria-label="From degree to desk."><span class="ln" aria-hidden="true"><span>From degree</span></span><span class="ln" aria-hidden="true"><span><em>to desk.</em></span></span></h1>
    <div class="hero__row">
      <p class="hero__lead" data-in="2">Practical accounts training for commerce graduates. Four months of the work an accounts office expects from day one.</p>
      <div>
        <div class="hero__act"><a class="btn btn--primary" href="#" data-counsel>Book counselling <span class="arr" aria-hidden="true"><svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M2 8h11M9 4l4 4-4 4"/></svg></span></a><a class="btn btn--line" href="#programme">See the programme</a></div>
        <p class="label hero__note">In person in Calicut — Batch dates will be announced soon.</p>
      </div>
    </div>
  </div>
  <div class="ticker" aria-hidden="true"><div class="ticker__track">{tick}</div></div>
</section>

<section class="sec gap">
  <div class="wrap">
    <p class="label" data-r>The gap</p>
    <h2 data-r>Plenty of openings. <em>Few ready hands.</em></h2>
    <p class="gap__t">Companies prefer people who can do the work from the first day. Most graduates have the degree, but have never posted a purchase bill, prepared a GST return or closed a month.</p>
    <p class="gap__p" data-r>Skills Lab closes that gap by doing the work. You learn each task the way an accounts office runs it, on real documents and in the software offices use, with practitioners beside you.</p>
  </div>
</section>

<section class="sec sec--cream" style="padding-block:clamp(56px,7vw,100px)">
  <div class="wrap">
    <p class="label" data-r>Brand position</p>
    <p class="pos__t" data-r style="--d:1">Numentis is the finance services group for businesses that take finance seriously — and the next generation of professionals who will run them.</p>
  </div>
</section>

<section class="sec" id="programme">
  <div class="wrap">
    <div class="glance">
      <div class="glance__stick">
        <p class="label">Basic Level</p>
        <h2>The Accounts Executive <em>programme.</em></h2>
        <p class="glance__sub">Six modules that follow money through a business: sales, purchases, books, banks, compliance and reporting, then a capstone and interview preparation.</p>
        <div class="now" aria-hidden="true"><div class="now__n metric" id="nowN">01<small>/ 06</small></div><p class="now__t" id="nowT">Post sales and purchase entries</p></div>
        <a class="btn btn--line glance__go" href="/programme">Full programme details <span class="arr" aria-hidden="true"><svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M2 8h11M9 4l4 4-4 4"/></svg></span></a>
      </div>
      <div>
        <p class="label" style="margin-bottom:18px">The work</p>
        <ul class="tasks">
{''.join(f'<li data-n="{i+1:02d}" data-t="{t}"><span class="code">{c}</span><div><h3>{t}</h3><span class="tool label">{tool}</span></div></li>' for i,(c,t,tool) in enumerate(TASKS))}
        </ul>
      </div>
    </div>
{stats()}
  </div>
</section>

<section class="sec sec--cream">
  <div class="wrap">
    <p class="label" data-r>Who it is for</p>
    <h2 class="who__h" data-r>If you studied commerce, <em>start here.</em></h2>
    <ul class="rows">
      <li data-r><span class="n">01</span><h3>Final-year commerce students</h3></li>
      <li data-r style="--d:1"><span class="n">02</span><h3>Fresh B.Com, M.Com, BBA and MBA graduates</h3></li>
      <li data-r style="--d:2"><span class="n">03</span><h3>Junior accountants in their first two years at work</h3></li>
    </ul>
  </div>
</section>

<section class="sec steps" id="admissions">
  <div class="wrap">
    <p class="label" data-r>Admissions</p>
    <h2 data-r>Three steps <em>to a seat.</em></h2>
    <p class="steps__intro" data-r>Batch dates will be announced soon. Seats are limited, so counselling comes first.</p>
    <div class="steps__grid">
      <div class="steps__line"><i></i></div>
      <div class="step"><span class="metric">01</span><h3>Talk to a counsellor</h3><p>In English or Malayalam, by phone, WhatsApp or in person. We check the programme fits you.</p></div>
      <div class="step"><span class="metric">02</span><h3>Choose how to pay</h3><p>₹50,000, or ₹40,000 if you pay in full at once. Instalments are available.</p></div>
      <div class="step"><span class="metric">03</span><h3>Confirm your seat</h3><p>Apply, confirm your seat, and join the batch when it starts.</p></div>
    </div>
  </div>
</section>

{cta()}
</main>
{footer()}
{DIALOG}
{SCRIPT}'''

MODS=[('Foundation and order-to-cash','Accounting as it is practised in an office: documents, entries and controls. Then the sales side: quotations, invoices, receivables, customer ledgers and collections.'),
('Procure-to-pay and inventory','Purchase orders, goods receipt, vendor bills, payables and payments, with stock records kept in step.'),
('Record-to-report and banking','From journals and ledgers to the trial balance and financial statements. Bank reconciliations, and the paperwork behind letters of credit and bank guarantees.'),
('Statutory compliance: TDS, GST, payroll','GST and TDS returns prepared under faculty supervision. Payroll with PF and ESI workings.'),
('Advanced tools: TallyPrime, ERP, Power BI','The same work done in the software offices use: TallyPrime, Zoho Books and ERP workflows, Excel for checks, and Power BI for reports.'),
('Capstone, interview preparation and graduation','A capstone that brings the five modules together, preparation for interviews, and graduation with the completion certificate.')]
TEACH=[('Taught by practitioners','People who do this work, not only teach it.'),('Built with hiring organisations','The curriculum was developed with the companies that hire accountants.'),('Real documents, real software','Invoices, bills, bank statements and returns, in TallyPrime, Zoho Books, Excel and Power BI.'),('Supervised compliance work','GST and TDS returns prepared under faculty supervision.'),('In person, in Calicut','Practical work needs a classroom and a teacher beside you.')]
FAQ=[('Who is the programme for?','Final-year commerce students, fresh B.Com, M.Com, BBA and MBA graduates, and junior accountants in their first two years at work. A counselling session confirms whether it fits you.'),
('How long is it, and where are classes held?','Four months, in six modules. Classes are in person, in our classroom in Calicut (Kozhikode).'),
('What does it cost?','The fee is ₹50,000. If you pay the full fee at once, it is ₹40,000. Instalment plans are explained at counselling.'),
('When does the next batch start?','Batch dates will be announced soon. Book a counselling session and we will tell you as soon as they are fixed.')]

prog=head('The Accounts Executive programme | Numentis Skills Lab','Six modules that follow money through a business, taught in person in Calicut. Four months. Fee ₹50,000.','programme')
prog+=f'''<main id="main">
<section class="phero">
  <div class="wrap">
    <p class="label">Basic Level</p>
    <h1 aria-label="The Accounts Executive programme."><span class="ln" aria-hidden="true"><span>The Accounts</span></span><span class="ln" aria-hidden="true"><span>Executive <em>programme.</em></span></span></h1>
    <p class="phero__lead" data-r>Six modules that follow money through a business: sales, purchases, books, banks, compliance and reporting, then a capstone and interview preparation.</p>
    <a class="btn btn--primary" href="#" data-counsel>Book counselling <span class="arr" aria-hidden="true"><svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M2 8h11M9 4l4 4-4 4"/></svg></span></a>
{stats()}
  </div>
</section>

<section class="sec sec--cream mods">
  <div class="wrap">
    <p class="label" data-r>Basic Level</p>
    <h2 data-r>The six <em>modules.</em></h2>
    <div class="stack">
{''.join(f'<article class="card" style="--k:{i}"><div><p class="label">Module</p><span class="metric">{i+1:02d}</span></div><div><h3>{t}</h3><p>{p}</p></div></article>' for i,(t,p) in enumerate(MODS))}
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <p class="label" data-r>Skills Lab</p>
    <h2 data-r style="font-size:clamp(2.2rem,5vw,4.4rem);margin-top:22px">How we <em>teach.</em></h2>
    <ul class="teach" style="margin-top:clamp(36px,5vw,64px)">
{''.join(f'<li data-r><h3>{t}</h3><p>{p}</p></li>' for t,p in TEACH)}
    </ul>
  </div>
</section>

<section class="sec sec--cream">
  <div class="wrap two">
    <div data-r><p class="label">Career readiness</p><h2>Ready for the interview, <em>and the first week.</em></h2></div>
    <div data-r style="--d:1">
      <ul class="ticks"><li>Interview preparation in the last module, including the practical questions employers ask</li><li>Guidance on where to apply and how to present the work you have done</li><li>A Numentis Skills Lab certificate of completion</li></ul>
      <div class="note"><p class="label">A note</p><p>We prepare you for interviews and guide your job search. We do not promise placement, interviews or salaries.</p></div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <p class="label" data-r>Fees</p>
    <h2 data-r style="font-size:clamp(2.2rem,5vw,4.4rem);margin-top:22px">What does it <em>cost?</em></h2>
    <div class="fees" data-r>
      <div><p class="label">Fee</p><span class="metric" data-count="50000" data-pre="₹">₹50,000</span></div>
      <div><p class="label">If you pay the full fee at once</p><span class="metric" data-count="40000" data-pre="₹">₹40,000</span></div>
    </div>
    <p class="fees__note" data-r>Instalment plans are explained at counselling.</p>
  </div>
</section>

<section class="sec sec--cream" id="questions">
  <div class="wrap">
    <p class="label" data-r>Questions</p>
    <h2 data-r style="font-size:clamp(2.2rem,5vw,4.4rem);margin-top:22px">Before you <em>ask.</em></h2>
    <div class="faq" data-r>
{''.join(f'<details><summary>{q}<i aria-hidden="true"></i></summary><p>{a}</p></details>' for q,a in FAQ)}
    </div>
  </div>
</section>

{cta().replace('sec sec--cream cta','sec cta')}
</main>
{footer()}
{DIALOG}
{SCRIPT}'''

import re
def rs(h):
    parts=re.split(r'(<[^>]+>)',h);o=[]
    for p_ in parts:
        o.append(p_ if p_.startswith('<') else p_.replace('₹','<span class="rs">₹</span>'))
    return ''.join(o)
home=rs(home);prog=rs(prog)
W=dict(encoding='utf-8',newline='\n')
(OUT/'index.html').write_text(home,**W)
(OUT/'programme.html').write_text(prog,**W)
(OUT/'vercel.json').write_text('{\n  "cleanUrls": true,\n  "rewrites": [{ "source": "/book", "destination": "/" }]\n}\n',**W)
kb=(OUT/'docs'/'knowledge-base.md').read_text(encoding='utf-8')
(OUT/'api'/'_kb.mjs').write_text('// Generated by tools/build_v2.py from docs/knowledge-base.md. Edit that file, not this one.\nexport const KB = '+json.dumps(kb,ensure_ascii=False)+';\n',**W)
print('built',len(home),len(prog))
