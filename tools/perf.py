import asyncio,json
from playwright.async_api import async_playwright
async def run(name,down,lat,cpu):
    async with async_playwright() as p:
        b=await p.chromium.launch();ctx=await b.new_context(viewport={'width':390,'height':844},device_scale_factor=2,is_mobile=True)
        pg=await ctx.new_page();c=await ctx.new_cdp_session(pg)
        await c.send('Network.enable');await c.send('Network.emulateNetworkConditions',{'offline':False,'downloadThroughput':down*1024/8,'uploadThroughput':down*1024/8/2,'latency':lat})
        await c.send('Emulation.setCPUThrottlingRate',{'rate':cpu})
        await pg.add_init_script("window.__m={};new PerformanceObserver(l=>{for(const e of l.getEntries())window.__m[e.entryType+(e.name?':'+e.name:'')]=e.startTime}).observe({type:'paint',buffered:true});new PerformanceObserver(l=>{for(const e of l.getEntries())window.__m.lcp=e.startTime}).observe({type:'largest-contentful-paint',buffered:true})")
        await pg.goto('http://127.0.0.1:8765/',wait_until='load')
        t=await pg.evaluate("performance.now()")
        await pg.wait_for_timeout(1500)
        m=await pg.evaluate("window.__m")
        bytes_=await pg.evaluate("performance.getEntriesByType('resource').reduce((a,e)=>a+e.transferSize,0)+performance.getEntriesByType('navigation')[0].transferSize")
        # time to open form after click
        await pg.evaluate("window.__t=performance.now()")
        await pg.click('.hero__act .btn--primary') if await pg.is_visible('.hero__act .btn--primary') else await pg.click('[data-counsel]')
        await pg.wait_for_selector('dialog[open]',timeout=5000)
        d=await pg.evaluate("performance.now()-window.__t")
        print(name,'load',round(t),'FCP',round(m.get('paint:first-contentful-paint',0)),'LCP',round(m.get('lcp',0)),'form opens in',round(d),'ms; bytes',bytes_)
        await b.close()
async def main():
    await run('4G-ish (9Mbps,170ms,4xCPU)',9000,170,4)
    await run('slow 3G-ish (1.6Mbps,400ms,6xCPU)',1600,400,6)
asyncio.run(main())
