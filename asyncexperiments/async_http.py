import asyncio
import aiohttp

from asyncexperiments.utils import async_timed
from asyncexperiments.async_utils.async_utils import fetch_status


fetch_status = async_timed()(fetch_status)


@async_timed()
async def main():
    session_timeout = aiohttp.ClientTimeout(total=50, connect=10)
    async with aiohttp.ClientSession(timeout=session_timeout) as session:
        url = 'https://www.yandex.ru'
        requests = [fetch_status(session, url) for _ in range(1000)]
        status_codes = await asyncio.gather(*requests, return_exceptions=True)
        exceptions = [res for res in status_codes if isinstance(res, Exception)]
        success = [res for res in status_codes if not isinstance(res, Exception)]
        print(f"Exceptions: {exceptions}")
        print(f"Result codes: {success}")
asyncio.run(main())

