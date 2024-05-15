import aiohttp
import asyncio
import logging
from asyncexperiments.async_utils.async_utils import fetch_status
from asyncexperiments.utils.async_timer import async_timed

@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        fetches = [asyncio.create_task(fetch_status(session, "https://google.com")),
                   asyncio.create_task(fetch_status(session, "ht://google.com")),
                   asyncio.create_task(fetch_status(session, "https://google.com"))]
        done, pending = await asyncio.wait(fetches, return_when=asyncio.FIRST_EXCEPTION)
        
        print(f"num of complided tasks: {len(done)}")
        print(f"num of waiting tasks: {len(pending)}")
        
        for done_task in done:
            if done_task.exception() is None:
                print(done_task.result())
            else:
                logging.error("During to call exception was rising",exc_info=done_task.exception())
        
        for pending_task in pending:
            pending_task.cancel()
            
asyncio.run(main())