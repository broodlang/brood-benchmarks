# A ring of N threads; a token travels around +1/hop for LAPS laps (N*LAPS hops).
# Checksum = N*LAPS.
import os, threading, queue
N = int(os.environ.get("BENCH_N", "200"))
LAPS = 5000
total = N * LAPS
inboxes = [queue.Queue() for _ in range(N)]
done = queue.Queue()


def node(i):
    inbox = inboxes[i]
    nxt = inboxes[(i + 1) % N]
    while True:
        v = inbox.get()
        if v >= total:
            done.put(v)
            return
        nxt.put(v + 1)


for i in range(N):
    threading.Thread(target=node, args=(i,), daemon=True).start()
inboxes[0].put(0)
print(done.get())
