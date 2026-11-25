import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch();pg=await b.new_page()
        await pg.goto('http://127.0.0.1:8765/?book&utm_source=meta');await pg.wait_for_timeout(600)
        print('opens on ?book:',await pg.evaluate("document.querySelector('dialog').open"))
        # simulate endpoint
        reqs=[]
        pg.on('request',lambda r:reqs.append((r.method,r.url,r.post_data)) if 'example.test' in r.url else None)
        await pg.route('https://example.test/**',lambda r:r.fulfill(status=200,body='ok'))
        await pg.evaluate("document.querySelector('#counsel form').setAttribute('data-endpoint','https://example.test/exec')")
        await pg.fill('#fullname','Test Student');await pg.fill('#mobile','+91 98765 43210');await pg.select_option('#who','Final-year student');await pg.check('#consent')
        await pg.click('#counsel button[type=submit]');await pg.wait_for_timeout(800)
        print('done shown:',await pg.evaluate("!document.querySelector('.done').hidden"),await pg.inner_text('.done .s'))
        print(reqs)
        await pg.goto('http://127.0.0.1:8765/');print('closed on normal:',not await pg.evaluate("document.querySelector('dialog').open"))
        await b.close()
asyncio.run(main())
