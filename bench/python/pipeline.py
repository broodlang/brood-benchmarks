import os
N = int(os.environ.get("BENCH_N", "200000"))

# map / filter / reduce pipeline: square the multiples of 3 or 5, sum the squares.
total = sum(i * i for i in range(N) if i % 3 == 0 or i % 5 == 0)
print(total)
