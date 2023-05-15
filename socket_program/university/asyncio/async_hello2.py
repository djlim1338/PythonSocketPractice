import asyncio
import time


async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)


async def main():
    start_time = time.time()
    print(f"started at {time.strftime('%X')}")
    await say_after(1, 'hello')
    await say_after(2, 'world')
    print(f"finished at {time.strftime('%X')}")
    print(f"걸린 시간 = {time.time() - start_time:.3f}초")

asyncio.run(main())
