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
    # close()+join(), NOT the `with` block: Pool.__exit__ calls terminate(), which KILLS
    # the workers instead of reaping them. Their CPU time is then never charged to this
    # process (getrusage only accounts waited-for children), so `/usr/bin/time` reported
    # ~0% CPU for a run that actually saturated every core — which made Python look like
    # the most CPU-efficient runtime in the suite. Joining makes the CPU-seconds column
    # true; it does not change the wall time being measured.
    # `fork`, not the 3.14 default `forkserver`: under forkserver the workers are children
    # of the forkserver process, never of this one, so this process reaps nothing and their
    # CPU time is invisible to getrusage/`/usr/bin/time`. Same parallelism either way.
    pool = mp.get_context("fork").Pool()
    total = sum(pool.map(work, range(TASKS)))
    pool.close()
    pool.join()
    print(total)
