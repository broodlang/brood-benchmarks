import os
N = int(os.environ.get("BENCH_N", "500000"))

best = 0
for start in range(1, N):
    n = start
    steps = 0
    while n != 1:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        steps += 1
    if steps > best:
        best = steps

print(best)
