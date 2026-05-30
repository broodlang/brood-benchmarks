import os
N = int(os.environ.get("BENCH_N", "128"))
MAXITER = 100

total = 0
for py in range(N):
    y0 = py / N * 3.0 - 1.5
    for px in range(N):
        x0 = px / N * 3.0 - 2.0
        x = 0.0
        y = 0.0
        i = 0
        while x * x + y * y <= 4.0 and i < MAXITER:
            xt = x * x - y * y + x0
            y = 2.0 * x * y + y0
            x = xt
            i += 1
        total += i

print(total)
