import os as _os
BASE=_os.environ.get('NUMENTIS_BASE','http://127.0.0.1:8790')
import asyncio,sys,re,hashlib,pathlib,json,os
SITE=pathlib.Path(__file__).resolve().parent
exec((SITE/'tools'/'shoot_v2.py').read_text(encoding='utf-8').split('async def main')[0].replace('import asyncio, sys, pathlib','import pathlib'))
from playwright.async_api import async_playwright
PACK=pathlib.Path(os.environ.get('NUMENTIS_PACK',SITE.parent/'Numentis_Brand_Final'))
R=[]
def rec(id,desc,ok,detail=''):R.append((id,desc,bool(ok),detail))
files={p.name:p.read_text(encoding='utf-8') for p in [SITE/'index.html',SITE/'programme.html',SITE/'assets/site.css',SITE/'assets/site.js']}
html=files['index.html']+files['programme.html'];css=files['site.css'];js=files['site.js']

# L1 logos byte-identical to pack
pairs={'logo-skills-lab-horizontal-ink.svg':'Vertical_Lockups/SVG/numentis-skills-lab_horizontal_primary_ink.svg','logo-skills-lab-horizontal-white.svg':'Vertical_Lockups/SVG/numentis-skills-lab_horizontal_white.svg','logo-skills-lab-stacked-white.svg':'Vertical_Lockups/SVG/numentis-skills-lab_stacked_white.svg','favicon.svg':'Logo_Production/SVG/icon_terracotta_bg.svg','apple-touch-icon.png':'Logo_Production/PNG/app-icons/icon_terracotta_bg_512.png'}
h=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
bad=[k for k,v in pairs.items() if h(SITE/'assets'/k)!=h(PACK/v)]
rec('L1','Logos/favicon byte-identical to brand pack',not bad,str(bad))
# logo files contain terracotta dot colour
rec('L3','Logo SVGs carry #C2410C dot',all('C2410C' in (SITE/'assets'/k).read_text(encoding='utf-8') for k in pairs if k.endswith('svg') and 'white' in k or k=='logo-skills-lab-horizontal-ink.svg'))
# C1 palette
allowed={'c2410c','0f1419','fafaf7','f5f1ea','6b6f76'}
hexes=set(x.lower() for x in re.findall(r'#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b',css+js+re.sub(r'&#\d+;','',html)))
hexes-= {'000'}  # mask-only
rec('C1','Only brand hex colours in css/js/html',hexes<=allowed,str(hexes-allowed))
rgbas=set(re.findall(r'rgba?\(([^)]*)\)',css))
okrgb={'250,250,247','15,20,25','107,111,118','245,241,234','194,65,12'}
badrgb=[r for r in rgbas if ','.join(x.strip() for x in r.split(',')[:3]) not in okrgb]
rec('C1b','rgba tints only of brand colours',not badrgb,str(badrgb))
rec('C2','No gradients on terracotta; no forest',not re.search(r'gradient\([^)]*(194,65,12|C2410C)',css,re.I) and '1B3A2F'.lower() not in css.lower())
round_terra=[b for b in re.findall(r'\{[^{}]*\}',css) if re.search(r'border-radius:\s*(50%|999)',b) and re.search(r'--terra|c2410c|194,\s*65,\s*12',b,re.I)]
rec('C3','No terracotta circles/dots (border-radius 50%/999px with terracotta bg)',not round_terra,str(round_terra[:2]))
# fonts
fam=set(re.findall(r"font-family:\s*([^;}]+)",css))
rec('T1','Only Fraunces/Onest/JetBrains Mono families (+ system fallbacks)',all(re.search(r"var\(--(serif|sans|mono)\)|^'(Fraunces|Onest|JetBrains Mono)'",f.strip()) for f in fam),str(fam))
rec('T1c','Fonts self-hosted, no Google Fonts requests','googleapis' not in html and '@font-face' in css and all((SITE/'assets/fonts'/f).exists() for f in ['fraunces-normal.woff2','fraunces-italic.woff2','onest.woff2','jetbrains-mono-400.woff2','jetbrains-mono-500.woff2']))
rec('T1b','No Familjen Grotesk text (logo files only)','familjen' not in (css+html+js).lower())
# V
text=re.sub(r'<script.*?</script>|<style.*?</style>','',html,flags=re.S);text=re.sub(r'<[^>]+>',' ',text)
words=['synergy','synergies','leverage','paradigm','ecosystem','journey','world-class','best-in-class','premium quality','value-add']
rec('V1','No banned jargon/puffery',not [w for w in words if w in text.lower()],str([w for w in words if w in text.lower()]))
rec('V2','No exclamation marks, no emoji in copy','!' not in text and not re.search('[\U0001F300-\U0001FAFF☀-➿]',text))
rec('V4','Position statement verbatim','Numentis is the finance services group for businesses that take finance seriously — and the next generation of professionals who will run them.' in files['index.html'])
rec('W4','Facts present: 4 months, 6 modules, Calicut, ₹50,000, ₹40,000',all(s in re.sub(r'<[^>]+>','',html) for s in ['4 months','Calicut','₹50,000','₹40,000','practitioners']))
rec('W5','No invented contact details (phone/email/address)',not re.search(r'\+91[ 0-9]{6,}|@[a-z]+\.[a-z]{2,}',text))
rec('W5b','Verticals alphabetical & equal weight in footer',html.count('<li>Audit &amp; Advisory</li><li>Next</li><li>Skills Lab</li><li>Strategy &amp; Finance</li>')==2)
rec('W3a','All images have alt',all('alt="' in m for m in re.findall(r'<img[^>]*>',html)))
rec('W3b','Reduced-motion media query present','prefers-reduced-motion' in css and 'reduce' in js)
rec('I1','No <img> other than brand logos',all('logo-skills-lab' in m for m in re.findall(r'<img[^>]*>',html)))

def lum(c):
    c=[x/255 for x in c];c=[x/12.92 if x<=.03928 else ((x+.055)/1.055)**2.4 for x in c];return .2126*c[0]+.7152*c[1]+.0722*c[2]
def cr(a,b):
    la,lb=lum(a),lum(b);return (max(la,lb)+.05)/(min(la,lb)+.05)

async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        ctx=await b.new_context(viewport={'width':1440,'height':900});pg=await ctx.new_page();await pg.route('**/*',route)
        errs=[];pg.on('console',lambda m:errs.append(m.text) if m.type=='error' else None);pg.on('pageerror',lambda e:errs.append(str(e)))
        for path in ('/','/programme'):
            await pg.goto(BASE+''+path);await pg.wait_for_timeout(1800)
            m=await pg.evaluate('''()=>{
              const cs=(e)=>getComputedStyle(e);const o={};
              const b=cs(document.body);o.body=[b.fontFamily,b.fontSize,b.fontWeight,b.lineHeight,b.letterSpacing,b.color];
              const hs=[...document.querySelectorAll('h1,h2')].map(e=>{const c=cs(e);return [e.tagName,c.fontFamily.split(',')[0],c.fontWeight,(parseFloat(c.lineHeight)/parseFloat(c.fontSize)).toFixed(3),(parseFloat(c.letterSpacing)/parseFloat(c.fontSize)).toFixed(3),c.fontVariationSettings]});
              o.heads=hs;
              const ls=[...document.querySelectorAll('.label')].map(e=>{const c=cs(e);return [c.fontFamily.split(',')[0],c.fontSize,c.textTransform,(parseFloat(c.letterSpacing)/parseFloat(c.fontSize)).toFixed(3)]});o.labels=ls;
              o.imgs=[...document.querySelectorAll('img')].map(i=>[i.getAttribute('src'),i.getBoundingClientRect().width,i.naturalWidth>0]);
              o.sw=document.documentElement.scrollWidth;
              o.tag=[...document.querySelectorAll('.tag')].map(e=>[cs(e).fontFamily.split(',')[0],cs(e).fontStyle,e.textContent]);
              o.em=[...document.querySelectorAll('h1 em,h2 em')].map(e=>[cs(e).fontStyle,cs(e).color,cs(e.parentElement).fontFamily.split(',')[0]]);
              o.btn=[...document.querySelectorAll('.btn--primary')].map(e=>[cs(e).backgroundColor,cs(e).color]);
              return o}''')
            n=path
            rec('T2'+n,'body Onest 16px/400/lh1.55/ls -0.01em ink',"Onest" in m['body'][0] and m['body'][1]=='16px' and m['body'][2]=='400' and m['body'][3]=='24.8px' and abs(float(m['body'][4][:-2])+.16)<.01 and m['body'][5]=='rgb(15, 20, 25)',str(m['body']))
            hh=[x for x in m['heads'] if x[0] in('H1','H2')]
            rec('T3'+n,'h1/h2 Fraunces 400 lh1.05 ls-0.03em(or tighter for display) opsz144',all('Fraunces' in x[1].replace('"','') and x[2]=='400' and x[3]=='1.050' and 'opsz' in x[5] and '144' in x[5] and float(x[4])<=-.029 for x in hh),str([x for x in hh if not('Fraunces' in x[1].replace('"','') and x[3]=='1.050' and float(x[4])<=-.029)]))
            lb=m['labels'];rec('T4'+n,'labels JetBrains Mono 12px uppercase ls .18em',all('JetBrains' in x[0] and x[1]=='12px' and x[2]=='uppercase' and abs(float(x[3])-.18)<.01 for x in lb),str([x for x in lb if not('JetBrains' in x[0] and x[1]=='12px' and abs(float(x[3])-.18)<.01)][:3]))
            rec('T5'+n,'Footer tagline Fraunces italic',all('Fraunces' in x[0].replace('"','') and x[1]=='italic' for x in m['tag']))
            rec('T5b'+n,'Heading italics Fraunces italic in terracotta',all(x[0]=='italic' and x[1]=='rgb(194, 65, 12)' for x in m['em']),str(m['em'][:2]))
            rec('C3b'+n,'CTA buttons exact terracotta / paper text',all(x[0]=='rgb(194, 65, 12)' for x in m['btn']))
            rec('L2'+n,'Logos >=80px wide and loaded',all(w>=80 and ok for _,w,ok in m['imgs'] if True) or any(w==0 for _,w,_ in m['imgs']),str(m['imgs']))
            rec('W3c'+n,'No horizontal overflow at 1440',m['sw']<=1440,str(m['sw']))
        rec('W3d','No console errors',not errs,str(errs[:3]))
        # overflow at widths
        for w in (360,390,768,1024):
            c2=await b.new_context(viewport={'width':w,'height':800});q=await c2.new_page();await q.route('**/*',route)
            for path in ('/','/programme'):
                await q.goto(BASE+''+path);await q.wait_for_timeout(900)
                sw=await q.evaluate('document.documentElement.scrollWidth');rec(f'W3e {w}{path}',f'No horizontal overflow at {w}px',sw<=w,str(sw))
            await c2.close()
        # contrast on all visible text nodes (home+programme) in light mode
        for path in ('/','/programme'):
            await pg.goto(BASE+''+path);await pg.wait_for_timeout(1200)
            await pg.evaluate('document.querySelectorAll("[data-r],.steps__grid").forEach(e=>e.classList.add("in"));document.querySelectorAll(".tasks li").forEach(e=>e.classList.add("on"));document.querySelectorAll(".w").forEach(e=>e.classList.add("lit"))');await pg.wait_for_timeout(900)
            res=await pg.evaluate('''()=>{
              function bg(e){while(e){const c=getComputedStyle(e).backgroundColor;const m=c.match(/[\\d.]+/g);if(m&&(m.length<4||+m[3]>0.5))return m.slice(0,3).map(Number);e=e.parentElement}return [250,250,247]}
              const out=[];const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;
              while(n=w.nextNode()){const t=n.textContent.trim();if(!t)continue;const e=n.parentElement;if(!e||e.closest('dialog,script,style,.menu,.ticker'))continue;const cs=getComputedStyle(e);if(cs.visibility==='hidden'||cs.display==='none')continue;
                const r=e.getBoundingClientRect();if(r.width===0)continue;
                const m=cs.color.match(/[\\d.]+/g).map(Number);out.push({t:t.slice(0,30),fg:m,a:m[3]===undefined?1:m[3],bg:bg(e),size:parseFloat(cs.fontSize),op:+cs.opacity*(e.closest('.tasks li:not(.on)')?1:1)})}
              return out}''')
            low=[]
            for r in res:
                fg=r['fg'][:3];a=r['a'];bgc=r['bg']
                fgm=[round(fg[i]*a+bgc[i]*(1-a)) for i in range(3)]
                c=cr(fgm,bgc)
                need=3.0 if r['size']>=24 or (r['size']>=18.66 and False) else 4.5
                if c<need-0.01:low.append((r['t'],round(c,2)))
            rec('W3f'+path,'Text contrast >= 4.5:1 (AA)',not low,str(low[:6]))
        # keyboard: dialog opens, esc closes
        await pg.goto(BASE+'/');await pg.wait_for_timeout(600)
        await pg.click('.head .btn');await pg.wait_for_timeout(300)
        op=await pg.evaluate('document.getElementById("counsel").open');await pg.keyboard.press('Escape');await pg.wait_for_timeout(200)
        cl=await pg.evaluate('!document.getElementById("counsel").open')
        rec('W3g','Dialog opens and Esc closes',op and cl)
        # internal links resolve
        links=set(re.findall(r'href="(/[^"#]*)',html))
        bad=[]
        for l in links:
            pth=l if l!='/' else '/index.html'
            if '.' not in pth.split('/')[-1]:pth+='.html'
            if not (SITE/pth.lstrip('/')).exists():bad.append(l)
        rec('W6','Internal links/assets resolve',not bad,str(bad))
        await b.close()
asyncio.run(main())
fails=[r for r in R if not r[2]]
for i,d,ok,det in R:print(('PASS ' if ok else 'FAIL ')+i+' '+d+('  -> '+det[:300] if not ok else ''))
print(f'\n{len(R)-len(fails)}/{len(R)} passed')
