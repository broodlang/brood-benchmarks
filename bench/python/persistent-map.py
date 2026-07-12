# Read-modify-write churn on a dict over a 50k key space.
# Checksum = sum of key*value over the map.
import os
N = int(os.environ.get("BENCH_N", "300000"))
M = 50000
x = 123456789
d = {}
for _ in range(N):
    x = (x * 1103515245 + 12345) & 0x7FFFFFFF
    key = x % M
    d[key] = d.get(key, 0) + 1 + (key % 7)
print(sum(k * v for k, v in d.items()))
