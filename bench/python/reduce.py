import os
from functools import reduce
from operator import add
N = int(os.environ.get("BENCH_N", "5000000"))

# higher-order fold: add applied per element (a real fold, not C-level sum()).
print(reduce(add, range(N), 0))
