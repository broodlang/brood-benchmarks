/* Integer arithmetic + tight inner loop. Longest Collatz chain below n.
 * Checksum = the maximum step count.
 *
 * No barrier: the chain length is data-dependent and genuinely unpredictable, so
 * the loop cannot be solved analytically. This is the row where C's branch-heavy
 * integer performance shows up honestly. */
#include "bench.h"

int main(void) {
    long n = bench_n(250000);
    long best = 0;
    for (long start = 1; start < n; start++) {
        long m = start, steps = 0;
        while (m != 1) {
            m = (m % 2 == 0) ? m / 2 : 3 * m + 1;
            steps++;
        }
        if (steps > best) best = steps;
    }
    printf("%ld\n", best);
    return 0;
}
