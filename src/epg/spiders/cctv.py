import asyncio
from operator import ge
from os import getpgrp
import time
import httpx
import ujson as json
import uvloop
from datetime import date

async def get_epg(channel_id, raw_date: date):
    headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"}
    url = 'https://api.cntv.cn/epg/getEpgInfoByChannelNew'
    async with httpx.AsyncClient() as client:
        current_time = time.time()
        res = await client.get(url, params={'c':f'{channel_id}', 'd':raw_date.strftime('%Y%m%d'), 'cb':'setItem1', 'serviceId':'tvcctv'}, headers=headers)
    raw_data = res.text[res.text.index('list') + 6:res.text.rindex('}}}')]
    list_data = json.loads(raw_data)
    #return list_data
    


if __name__ == "__main__":
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = asyncio.get_event_loop()
    start = time.perf_counter()
    loop.run_until_complete(get_epg('cctv2', date.today()))
    end = time.perf_counter()
    print(f"用时{end - start}s")