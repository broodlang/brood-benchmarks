import os
N = int(os.environ.get("BENCH_N", "80"))
MOD = 1000000007

A = [[(i + j) % 100 for j in range(N)] for i in range(N)]
B = [[(i * j) % 100 for j in range(N)] for i in range(N)]

total = 0
for i in range(N):
    Ai = A[i]
    for j in range(N):
        s = 0
        for k in range(N):
            s += Ai[k] * B[k][j]
        total += s

print(total % MOD)
