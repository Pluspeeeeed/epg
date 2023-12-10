import asyncio
from datetime import date
import time
import httpx
import ujson as json
import uvloop

async def get_epg(channel_id, raw_date: date):
    headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"}
    url = 'http://module.iqilu.com/media/apis/main/getprograms'
    async with httpx.AsyncClient() as client:
        current_time = time.time()
        res = await client.get(url, params={'jsonpcallback':current_time, 'channelID': channel_id, 'date': raw_date.strftime('%Y-%m-%d')}, headers=headers)
    raw_data = res.text[res.text.index('list') + 6:res.text.rindex('now') - 2]
    list_data = json.loads(raw_data)
    #return list_data
    


if __name__ == "__main__":
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = asyncio.get_event_loop()
    start = time.perf_counter()
    loop.run_until_complete(get_epg(25, date.today()))
    end = time.perf_counter()
    print(f"用时{end - start}s")