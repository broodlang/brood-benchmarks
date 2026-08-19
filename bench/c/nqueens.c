/* Backtracking recursion — count N-queens solutions. Checksum = 724 at n=10.
 *
 * `placed` holds the column chosen for each row above, and `safe` walks it
 * NEAREST ROW FIRST with the row distance counting up from 1 — the same traversal
 * the Brood (`(cons c placed)`) and Node (`[c, ...placed]`) ports do.
 *
 * C pushes onto a stack array, which is O(1), matching Brood's O(1) `cons`. Node's
 * spread is an O(n) copy and .NET's `new List(...)` likewise; that difference is
 * already inherent between the existing columns, so C sitting on the cons side of
 * it is not a liberty taken here.
 *
 * No barrier: the solution count is a data-dependent search. */
#include "bench.h"

static long n;
static int placed[32];

static int safe(int c, int row) {
    int d = 1;
    for (int i = row - 1; i >= 0; i--) { /* nearest row first */
        int p = placed[i];
        if (p == c || p - c == d || p - c == -d) return 0;
        d++;
    }
    return 1;
}

static long solve(int row) {
    if (row == n) return 1;
    long total = 0;
    for (int c = 0; c < n; c++) {
        if (safe(c, row)) {
            placed[row] = c;
            total += solve(row + 1);
        }
    }
    return total;
}

int main(void) {
    n = bench_n(10);
    if (n > 32) return 1;
    printf("%ld\n", solve(0));
    return 0;
}
