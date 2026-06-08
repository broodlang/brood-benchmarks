# Fan out N asyncio coroutines, each returning its index; gather and sum.
# asyncio coroutines are Python's lightest concurrent unit — a single OS thread
# runs them all co-operatively on the event loop. Checksum = N*(N-1)/2.
import asyncio
import os

N = int(os.environ.get("BENCH_N", "20000"))


async def worker(i):
    return i


async def main():
    results = await asyncio.gather(*(worker(i) for i in range(N)))
    print(sum(results))


asyncio.run(main())
