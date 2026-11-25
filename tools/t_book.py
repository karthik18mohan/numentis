import os as _os
BASE=_os.environ.get('NUMENTIS_BASE','http://127.0.0.1:8790')
import asyncio,json
from playwright.async_api import async_playwright

async def submit(pg,delivered):
    reqs=[]
    async def fake(r):
        reqs.append(json.loads(r.request.post_data));await r.fulfill(status=200,content_type='application/json',body=json.dumps({'ok':True,'delivered':delivered}))
    await pg.route('**/api/lead',fake)
    await pg.goto(BASE+'/?book&utm_source=meta&utm_campaign=nov');await pg.wait_for_timeout(600)
    opened=await pg.evaluate("document.querySelector('dialog').open")
    await pg.fill('#fullname','Test Student');await pg.fill('#mobile','+91 98765 43210');await pg.select_option('#who','Final-year student');await pg.check('#consent')
    await pg.click('#counsel button[type=submit]');await pg.wait_for_timeout(800)
    done=await pg.evaluate("!document.querySelector('.done').hidden");msg=await pg.inner_text('.done .s')
    await pg.unroute('**/api/lead')
    return opened,done,msg,reqs

async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch();pg=await b.new_page()
        opened,done,msg,reqs=await submit(pg,True)
        print('opens on ?book:',opened)
        print('live: done shown:',done,'|',msg)
        print('lead sent with utm:',bool(reqs) and reqs[0]['source']=='meta' and reqs[0]['campaign']=='nov' and reqs[0]['consent']=='yes')
        _,done,msg,_=await submit(pg,False)
        print('preview: done shown:',done,'|',msg)
        await pg.goto(BASE+'/');print('closed on normal:',not await pg.evaluate("document.querySelector('dialog').open"))
        await b.close()
asyncio.run(main())
