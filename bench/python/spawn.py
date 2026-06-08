# Fan out N asyncio coroutines; each computes fib(15) and returns the result.
# Tests coroutine fan-out under real CPU work per unit.
# Checksum = N * fib(15) = N * 610.
import asyncio
import os

N = int(os.environ.get("BENCH_N", "20000"))


def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)


async def worker():
    return fib(15)


async def main():
    results = await asyncio.gather(*(worker() for _ in range(N)))
    print(sum(results))


asyncio.run(main())
