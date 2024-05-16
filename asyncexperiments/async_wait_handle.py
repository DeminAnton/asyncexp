import logging
import asyncio
import aiohttp
from async_utils.async_utils import fetch_status
from utils.async_timer import async_timed



async def successful_task(session, url):
    await fetch_status(session, url)
    return f'Successful task completed'

async def failing_task(n):
    await asyncio.sleep(n)
    raise ValueError(f'Failing task {n} encountered an error')

@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [
            asyncio.create_task(successful_task(session, "https://google.com")),
            asyncio.create_task(failing_task(1)),
            asyncio.create_task(successful_task(session, "https://google.com")),
            asyncio.create_task(failing_task(2))
        ]
    
        # Wait for the tasks, returning when the first task raises an exception
        done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_EXCEPTION)
    
        # Handling completed tasks
        for task in done:
            if task.exception():
                print(f'Task raised an exception: {task.exception()}')
            else:
                print(f'Task result: {task.result()}')
    
        # Handling pending tasks
        if pending:
            print(f'{len(pending)} tasks are still pending. Cancelling them...')
            for task in pending:
                # Cancel the pending task
                task.cancel()
                try:
                    # Await the task to ensure it has processed the cancellation
                    await task
                except asyncio.CancelledError:
                    # Catch the cancellation exception to confirm the task was cancelled
                    logging.warning(f"task {task} was cancelled")

asyncio.run(main())
