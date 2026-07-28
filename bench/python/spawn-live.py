# Hold N units alive, then hand each a message it must COPY. The copy is what makes
# this comparable to a process runtime: on the BEAM and in Brood, `send` copies, so the
# receiver cannot observe the sender's later mutations. An asyncio task receiving a
# reference is a different and much cheaper operation.
#
# A Python task is not an isolated process — one shared heap, no mailbox, no preemption,
# and one thread. See BENCHMARKS.md. Checksum = N * (sum(payload) + 1).
import asyncio
import os

N = int(os.environ.get("BENCH_N", "300000"))
PAYLOAD = list(range(16))


async def unit(fut):
    p = await fut
    return sum(p) + 1


async def main():
    loop = asyncio.get_running_loop()
    futs = [loop.create_future() for _ in range(N)]
    tasks = [asyncio.create_task(unit(f)) for f in futs]
    for f in futs:
        f.set_result(list(PAYLOAD))          # copy, as `send` would
    total = 0
    for chunk in range(0, N, 10000):
        total += sum(await asyncio.gather(*tasks[chunk:chunk + 10000]))
    print(total)


asyncio.run(main())
