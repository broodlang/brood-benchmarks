# Generate N decimal strings; count full matches of [0-9]+. Checksum = count.
import os, re
N = int(os.environ.get("BENCH_N", "20000"))
pat = re.compile(r"[0-9]+")
x = 123456789
count = 0
for _ in range(N):
    x = (x * 1103515245 + 12345) & 0x7FFFFFFF
    s = str(x)
    if x % 2 == 0:
        s += "x"
    if pat.fullmatch(s):
        count += 1
print(count)
