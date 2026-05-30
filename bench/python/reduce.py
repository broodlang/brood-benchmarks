import os
N = int(os.environ.get("BENCH_N", "1000000"))

# idiomatic fast fold for addition over a range
print(sum(range(N)))
