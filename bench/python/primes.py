import os
N = int(os.environ.get("BENCH_N", "20000"))

def is_prime(n):
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True

count = 0
for n in range(2, N):
    if is_prime(n):
        count += 1

print(count)
