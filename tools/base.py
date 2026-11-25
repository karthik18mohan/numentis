import os as _os
BASE=_os.environ.get('NUMENTIS_BASE','http://127.0.0.1:8790')
import asyncio,sys
from playwright.async_api import async_playwright
JS='''()=>{const h=document.querySelector('.hero'),rl=(()=>{const d=document.createElement('div');d.style.cssText='height:var(--rl);position:absolute';h.appendChild(d);const v=d.getBoundingClientRect().height;d.remove();return v})(),top=h.getBoundingClientRect().top;
function bl(el){const s=document.createElement('span');s.style.cssText='display:inline-block;width:0;height:0';el.appendChild(s);const y=s.getBoundingClientRect().bottom-top;s.remove();return y}
const out={rl:rl};
out.eyebrow=bl(document.querySelector('.hero__eyebrow .label'));
const ln=document.querySelectorAll('.hero h1 .ln>span');out.h1a=bl(ln[0]);out.h1b=bl(ln[1]);
const lead=document.querySelector('.hero__lead');out.lead=bl(lead);out.leadH=lead.getBoundingClientRect().height;
const b=document.querySelector('.hero__act .btn').getBoundingClientRect();out.btnTop=b.top-top;out.btnBot=b.bottom-top;
out.note=bl(document.querySelector('.hero__note'));out.rowBot=document.querySelector('.hero__row').getBoundingClientRect().bottom-top;
const t=document.querySelector('.ticker').getBoundingClientRect();out.tick=t.top-top;out.hero=h.getBoundingClientRect().height;
return out}'''
async def main(w,hh):
    async with async_playwright() as p:
        b=await p.chromium.launch();pg=await b.new_page(viewport={'width':w,'height':hh})
        await pg.route('**/fonts.g*',lambda r:r.abort())
        await pg.goto(BASE+'/');await pg.wait_for_timeout(2500)
        o=await pg.evaluate(JS);rl=o['rl'];print(o)
        # baseline - line positions: targets k*rl-1
        T={'eyebrow':2,'h1a':5,'h1b':8,'lead':13}
        for k,m in T.items():
            if m: print(k,'err px',round(o[k]-(m*rl-1),2))
        print('note err',round(o['note']-(o['rowBot']-1),2),'rowBot/rl',o['rowBot']/rl);print('btn top/rl',o['btnTop']/rl,'bot/rl',o['btnBot']/rl,'note/rl',o['note']/rl,'tick',o['tick']/rl)
        await b.close()
asyncio.run(main(int(sys.argv[1]),int(sys.argv[2])))
