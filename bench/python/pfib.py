# Parallel fib: compute fib(N) in 100 tasks at once, summed. Python's GIL means
# threads give no CPU speedup, so the idiomatic way to use cores is a process
# pool (default size = os.cpu_count()). Checksum = 100*fib(N).
import os
import multiprocessing as mp

N = int(os.environ.get("BENCH_N", "31"))
TASKS = 100


def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


def work(_):
    return fib(N)


if __name__ == "__main__":
    with mp.Pool() as pool:
        total = sum(pool.map(work, range(TASKS)))
    print(total)
