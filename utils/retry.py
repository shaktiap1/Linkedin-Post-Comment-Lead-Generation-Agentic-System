import asyncio
from functools import wraps


def async_retry(retries=3, delay=2):

    def decorator(func):

        @wraps(func)
        async def wrapper(*args, **kwargs):

            last_exception = None

            for attempt in range(retries):

                try:
                    return await func(*args, **kwargs)

                except Exception as e:

                    last_exception = e

                    if attempt < retries - 1:
                        await asyncio.sleep(delay)

            raise last_exception

        return wrapper

    return decorator

'''
Iska Use Kaise Hoga

Later scraper me:   


Agar scraping fail ho jaye:

retry automatically trigger hoga aur retry limit ke hisab se retry karega
'''