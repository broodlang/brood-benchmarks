import os
N = int(os.environ.get("BENCH_N", "540"))
MAXITER = 100

total = 0
for py in range(N):
    y0 = py / N * 3.0 - 1.5
    for px in range(N):
        x0 = px / N * 3.0 - 2.0
        x = 0.0
        y = 0.0
        i = 0
        xx = 0.0
        yy = 0.0
        while xx + yy <= 4.0 and i < MAXITER:
            y = 2.0 * x * y + y0   # uses old x, old y
            x = xx - yy + x0       # uses old xx, yy
            xx = x * x
            yy = y * y
            i += 1
        total += i

print(total)
