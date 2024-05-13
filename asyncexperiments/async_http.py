import asyncio
import aiohttp

from aiohttp import ClientSession
from asyncexperiments.utils import async_timed
from asyncexperiments.async_utils.async_utils import fetch_status


fetch_status = async_timed()(fetch_status)


@async_timed()
async def main():
    session_timeout = aiohttp.ClientTimeout(total=50, connect=10)
    async with aiohttp.ClientSession(timeout=session_timeout) as session:
        url = 'https://www.example.com'
        requests = [fetch_status(session, url) for _ in range(1000)]
        status_codes = await asyncio.gather(*requests)
        print(status_codes)

asyncio.run(main())