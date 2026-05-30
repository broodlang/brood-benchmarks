import os, sys
sys.setrecursionlimit(100000)
N = int(os.environ.get("BENCH_N", "40"))   # repetitions
DEPTH = 12

def make(d):
    if d == 0:
        return None
    return (make(d - 1), make(d - 1))

def check(node):
    if node is None:
        return 1
    return 1 + check(node[0]) + check(node[1])

total = 0
for _ in range(N):
    total += check(make(DEPTH))

print(total)
