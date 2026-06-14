import os, sys
sys.setrecursionlimit(100000)
N = int(os.environ.get("BENCH_N", "37"))

def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

print(fib(N))
