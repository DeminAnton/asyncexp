import functools
import time
from typing import Callable, Any

def async_timed():
    """
    A decorator that measures the execution time of an asynchronous function.

    This decorator can be applied to any asynchronous function to log its execution time.
    When the function is called, it logs the function details (including arguments) before
    execution, and the total execution time after the function completes. The execution
    time is measured using the `time.time()` method from the `time` module.

    Returns:
        Callable: A decorator that wraps the asynchronous function, adding logging
        and timing functionality.

    Example:
        >>> @async_timed()
        ... async def sample_async_func(x):
        ...     import asyncio
        ...     await asyncio.sleep(x)
        ...     return x
        ...
        >>> import asyncio
        >>> asyncio.run(sample_async_func(2))
        executed <function sample_async_func at 0x...> with arguments (2,) {}
        <function sample_async_func at 0x...> completed in 2.0 sec.
        2

    Note:
        - The decorator assumes that the wrapped function is an async function.
        - Time measurement may be affected by system load and other asynchronous tasks running
          concurrently.
    """
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapped(*args, **kwargs) -> Any:
            print(f'executed {func} with arguments {args} {kwargs}')
            start = time.time()
            try:
                return await func(*args, **kwargs)
            finally:
                end = time.time()
                total = end - start
                print(f'{func} complited in {total} sec.')
        return wrapped
    return wrapper
