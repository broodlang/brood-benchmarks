import os
n = int(os.environ.get("BENCH_N", "200000"))
md = 1000000007

class BenchError(Exception):
    pass

acc = 0
for i in range(n):
    try:
        raise BenchError(i % 100)
    except BenchError as e:
        acc += e.args[0]

print(acc % md)
