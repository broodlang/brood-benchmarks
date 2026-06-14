import os
N = int(os.environ.get("BENCH_N", "30000000"))

acc = 0
i = 0
while i < N:
    acc += i
    i += 1

print(acc)
