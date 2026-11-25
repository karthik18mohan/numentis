import os as _os
BASE=_os.environ.get('NUMENTIS_BASE','http://127.0.0.1:8790')
import asyncio, sys, pathlib
sys.path.insert(0,'.')
from playwright.async_api import async_playwright
S=pathlib.Path('/tmp/claude-0/-home-claude/908d83fa-d3c9-5295-8784-9fe47775133a/scratchpad')
F=S/'fonts/node_modules'
fonts={'fraunces-n.woff2':F/'@fontsource-variable/fraunces/files/fraunces-latin-full-normal.woff2','fraunces-i.woff2':F/'@fontsource-variable/fraunces/files/fraunces-latin-full-italic.woff2','onest.woff2':F/'@fontsource-variable/onest/files/onest-latin-wght-normal.woff2','jb4.woff2':F/'@fontsource/jetbrains-mono/files/jetbrains-mono-latin-400-normal.woff2','jb5.woff2':F/'@fontsource/jetbrains-mono/files/jetbrains-mono-latin-500-normal.woff2'}
CSS="""
@font-face{font-family:'Fraunces';font-style:normal;font-weight:300 600;src:url(https://fonts.gstatic.com/l/fraunces-n.woff2) format('woff2')}
@font-face{font-family:'Fraunces';font-style:italic;font-weight:300 600;src:url(https://fonts.gstatic.com/l/fraunces-i.woff2) format('woff2')}
@font-face{font-family:'Onest';font-style:normal;font-weight:300 600;src:url(https://fonts.gstatic.com/l/onest.woff2) format('woff2')}
@font-face{font-family:'JetBrains Mono';font-style:normal;font-weight:400;src:url(https://fonts.gstatic.com/l/jb4.woff2) format('woff2')}
@font-face{font-family:'JetBrains Mono';font-style:normal;font-weight:500;src:url(https://fonts.gstatic.com/l/jb5.woff2) format('woff2')}
"""
async def route(r):
    u=r.request.url
    if 'fonts.googleapis.com' in u: await r.fulfill(status=200,content_type='text/css',body=CSS)
    elif 'fonts.gstatic.com/l/' in u: await r.fulfill(status=200,content_type='font/woff2',body=fonts[u.rsplit('/',1)[1]].read_bytes())
    elif 'fonts.gstatic.com' in u: await r.abort()
    else: await r.continue_()
async def main(out):
    o=pathlib.Path(out);o.mkdir(exist_ok=True,parents=True)
    async with async_playwright() as p:
        b=await p.chromium.launch()
        for lab,vp,dsf in (('desk',{'width':1440,'height':900},1),('mob',{'width':390,'height':844},2)):
            ctx=await b.new_context(viewport=vp,device_scale_factor=dsf);pg=await ctx.new_page();logs=[]
            pg.on('console',lambda m:logs.append(m.type+': '+m.text) if m.type in('error','warning') else None)
            pg.on('pageerror',lambda e:logs.append('PAGEERROR '+str(e)))
            await pg.route('**/*',route)
            for name,path in (('home','/'),('prog','/programme')):
                await pg.goto(BASE+''+path);await pg.wait_for_timeout(2200)
                await pg.screenshot(path=str(o/f'{lab}-{name}-fold.png'))
                # scroll through to trigger observers
                h=await pg.evaluate('document.documentElement.scrollHeight');y=0
                while y<h:
                    await pg.evaluate(f'window.scrollTo(0,{y})');await pg.wait_for_timeout(180);y+=500
                await pg.evaluate('window.scrollTo(0,0)');await pg.wait_for_timeout(600)
                await pg.screenshot(path=str(o/f'{lab}-{name}.png'),full_page=True)
            print(lab,logs[:6])
            await ctx.close()
        await b.close()
asyncio.run(main(sys.argv[1]))
