import os, sys
n = int(os.environ.get("BENCH_N", "50000"))
md = 1000000007
DEPTH = 50
sys.setrecursionlimit(10000)

class BenchError(Exception):
    pass

def descend(d, i):
    if d == 0:
        raise BenchError(i % 100)
    return 1 + descend(d - 1, i)

acc = 0
for i in range(n):
    try:
        descend(DEPTH, i)
    except BenchError as e:
        acc += e.args[0]
print(acc % md)
