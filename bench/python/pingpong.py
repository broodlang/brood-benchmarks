# Two threads bounce a token N round trips via queues. Checksum = N.
import os, threading, queue
N = int(os.environ.get("BENCH_N", "100000"))
q_to = queue.Queue()
q_from = queue.Queue()


def responder():
    while True:
        m = q_to.get()
        if m < 0:
            break
        q_from.put(m)


t = threading.Thread(target=responder)
t.start()
k = 0
while k < N:
    q_to.put(k)
    q_from.get()
    k += 1
q_to.put(-1)
t.join()
print(k)
