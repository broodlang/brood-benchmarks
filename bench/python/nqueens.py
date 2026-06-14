import os
import sys
sys.setrecursionlimit(10000)
N = int(os.environ.get("BENCH_N", "10"))


def safe(c, placed, d):
    for p in placed:
        if p == c or p - c == d or p - c == -d:
            return False
        d += 1
    return True


def solve(row, placed):
    if row == N:
        return 1
    total = 0
    for c in range(N):
        if safe(c, placed, 1):
            total += solve(row + 1, [c] + placed)
    return total


print(solve(0, []))
