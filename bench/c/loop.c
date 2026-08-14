/* Raw iteration. Sum 0..n-1, checksum = n(n-1)/2.
 *
 * This is the row most at risk of a compiler solving it analytically instead of
 * running it, so it is the row whose machine code was actually inspected rather
 * than assumed. On GCC 15.2.0 at -O2 -march=native it is NOT closed-formed: the
 * asm has a real loop back-edge, no SIMD, and none of the imul/shr markers a
 * closed form would leave. It executes 30,000,000 real iterations.
 *
 * Evidence, kept here because the next compiler upgrade should re-check it:
 *   -O0                     60 ms
 *   -O2                      8 ms   (~0.9 cycles/iteration — unrolled scalar adds)
 *   a closed form would be ~0.4 ms  (bare process startup)
 *
 * An earlier version of this file forced iteration with an asm barrier. That was
 * removed: it did not prevent elision (there was none), it just cost 50% — 12 ms
 * against 8 ms — by pinning the accumulator every pass. Handicapping C on a
 * premise that turns out to be false is the same error as flattering it.
 *
 * See bench/c/bench.h for the full audit. */
#include "bench.h"

int main(void) {
    long n = bench_n(30000000);
    long acc = 0;
    for (long i = 0; i < n; i++) acc += i;
    printf("%ld\n", acc);
    return 0;
}
