import os
N = int(os.environ.get("BENCH_N", "100000"))
K = 1000

x = 123456789
counts = {}
for _ in range(N):
    x = (x * 1103515245 + 12345) & 0x7FFFFFFF
    key = x % K
    counts[key] = counts.get(key, 0) + 1

total = 0
for k, v in counts.items():
    total += k * v

print(total)
