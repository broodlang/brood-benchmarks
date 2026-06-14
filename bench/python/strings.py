import os
N = int(os.environ.get("BENCH_N", "1000000"))

s = ",".join(str(i) for i in range(N))
print(len(s))
