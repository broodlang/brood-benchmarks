# Sieve of Eratosthenes to N, counting primes. Checksum = count of primes <= N.
import os
N = int(os.environ.get("BENCH_N", "1000000"))
comp = bytearray(N + 1)
p = 2
while p * p <= N:
    if not comp[p]:
        for j in range(p * p, N + 1, p):
            comp[j] = 1
    p += 1
count = 0
for k in range(2, N + 1):
    if not comp[k]:
        count += 1
print(count)
