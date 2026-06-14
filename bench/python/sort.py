import os
N = int(os.environ.get("BENCH_N", "375000"))
MOD = 1000000007

x = 123456789
data = []
for _ in range(N):
    x = (x * 1103515245 + 12345) & 0x7FFFFFFF
    data.append(x)

data.sort()

h = 0
for v in data:
    h = (h * 31 + v) % MOD

print(h)
