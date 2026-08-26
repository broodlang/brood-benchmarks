import os
N = int(os.environ.get("BENCH_N", "30000000"))
acc = 0
for i in range(N):
    acc += i
print(acc)
