# Ackermann ack(3,9) summed N times. Deep double-recursion (depth ~4093).
# Checksum = N * ack(3,9) = N * 4093.
import os, sys, threading
sys.setrecursionlimit(1_000_000)
N = int(os.environ.get("BENCH_N", "6"))


def ack(m, k):
    if m == 0:
        return k + 1
    if k == 0:
        return ack(m - 1, 1)
    return ack(m - 1, ack(m, k - 1))


def main():
    total = 0
    for _ in range(N):
        total += ack(3, 9)
    print(total)


# run on a thread with a large C stack so depth ~4093 never overflows
threading.stack_size(256 * 1024 * 1024)
t = threading.Thread(target=main)
t.start()
t.join()
