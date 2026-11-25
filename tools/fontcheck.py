import os as _os
BASE=_os.environ.get('NUMENTIS_BASE','http://127.0.0.1:8790')
import asyncio,sys
exec(open('shoot_v2.py').read().split('async def main')[0])
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch();ctx=await b.new_context(viewport={'width':1440,'height':900});pg=await ctx.new_page();await pg.route('**/*',route)
        cdp=await ctx.new_cdp_session(pg)
        for path in ('/','/programme'):
            await pg.goto(BASE+''+path);await pg.wait_for_timeout(1500)
            await pg.evaluate('document.querySelectorAll("[data-r]").forEach(e=>e.classList.add("in"))')
            await cdp.send('DOM.enable');await cdp.send('CSS.enable')
            doc=await cdp.send('DOM.getDocument',{'depth':-1})
            res=await cdp.send('DOM.querySelectorAll',{'nodeId':doc['root']['nodeId'],'selector':'body *'})
            seen={}
            for nid in res['nodeIds']:
                try:
                    f=await cdp.send('CSS.getPlatformFontsForNode',{'nodeId':nid})
                except Exception:continue
                for x in f['fonts']:
                    k=(x['familyName'],x.get('isCustomFont'))
                    seen[k]=seen.get(k,0)+x['glyphCount']
            print(path,seen)
        await b.close()
asyncio.run(main())
