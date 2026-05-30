import os
from functools import reduce
N = int(os.environ.get("BENCH_N", "1000000"))

print(reduce(lambda a, b: a + b, range(N), 0))
