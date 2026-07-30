# Hold N units alive, then hand each a message it must COPY, and collect each result
# through a queue the parent drains one at a time — mirroring a mailbox.
#
# Fairness fix (2026-07-30): the result path was `asyncio.gather` over a task list, i.e.
# a reference store per unit. Brood and Elixir send a reply *message* the parent receives
# individually, so they were paying 2 copied messages per unit against Python's 1
# delivery + 0. An `asyncio.Queue` drained one item at a time is the honest analogue.
# (The inbound copy was already here: a task receiving a reference is a different and
# much cheaper operation than `send`.)
#
# A Python task is not an isolated process — one shared heap, no preemption, one thread.
# See BENCHMARKS.md. Checksum = N * (sum(payload) + 1).
import asyncio
import os

N = int(os.environ.get("BENCH_N", "300000"))
PAYLOAD = list(range(16))


async def unit(fut, box):
    p = await fut
    await box.put(sum(p) + 1)            # reply as a message, not a return value


async def main():
    loop = asyncio.get_running_loop()
    box = asyncio.Queue()
    futs = [loop.create_future() for _ in range(N)]
    tasks = [asyncio.create_task(unit(f, box)) for f in futs]
    for f in futs:
        f.set_result(list(PAYLOAD))      # copy, as `send` would
    total = 0
    for _ in range(N):
        total += await box.get()
    await asyncio.gather(*tasks)
    print(total)


asyncio.run(main())
