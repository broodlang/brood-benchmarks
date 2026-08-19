/* Deep double-recursion. ack(3,9) summed n times; checksum = n * 4093.
 *
 * Recursion depth reaches ~4093. C's default 8 MB stack holds that comfortably
 * (the .NET port needs an explicit 256 MB thread because its frames are far
 * larger), so no thread juggling here.
 *
 * No barrier: ackermann is not analytically reducible by any compiler. GCC will
 * turn the `k == 0` arm into a tail call, which is a legitimate optimisation every
 * other runtime in this suite is also free to make. */
#include "bench.h"

static long ack(long m, long k) {
    if (m == 0) return k + 1;
    if (k == 0) return ack(m - 1, 1);
    return ack(m - 1, ack(m, k - 1));
}

int main(void) {
    long n = bench_n(6);
    long total = 0;
    for (long i = 0; i < n; i++) total += ack(3, 9);
    printf("%ld\n", total);
    return 0;
}
