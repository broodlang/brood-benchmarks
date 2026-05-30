import os
N = int(os.environ.get("BENCH_N", "3000000"))

acc = 0
i = 0
while i < N:
    acc += 1
    i += 1

print(acc)
