import asyncio
import random


async def human_delay(min_delay=1.2, max_delay=3.5):

    delay = random.uniform(min_delay, max_delay)

    await asyncio.sleep(delay)