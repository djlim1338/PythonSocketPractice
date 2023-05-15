import asyncio
import time


async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)


async def main():
    start_time = time.time()
    task1 = asyncio.create_task(say_after(1, 'hello'))
    task2 = asyncio.create_task(say_after(2, 'world'))
    print(f"started at {time.strftime('%X')}")
    # Wait until both tasks are completed
    # should take around 2 seconds.
    await task1
    await task2
    print(f"finished at {time.strftime('%X')}")
    print(f"걸린 시간 = {time.time() - start_time:.3f}초")

asyncio.run(main())
