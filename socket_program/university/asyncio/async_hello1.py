"""

async_hello.py

"""
import asyncio


async def hello():
    print("hello")
    await asyncio.sleep(1)
    print('world')

asyncio.run(hello())

