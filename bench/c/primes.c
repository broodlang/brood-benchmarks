/* Integer arithmetic (trial division). Count primes below n; checksum = 13848 at n=150000.
 *
 * Uses `int`, not `long`, because every other port does: the C# port is `int`, and
 * JS/Brood integers in this range are 32-bit-ish too. It matters more than it looks
 * — x86 `idivl` is materially cheaper than `idivq`, and trial division is nothing
 * but division. Measured on this machine: 14 ms with `long` against 9 ms with `int`,
 * i.e. the `long` version was charging C 55% for a width no other column uses.
 *
 * Hoists the sqrt bound out of the inner loop, matching the C#/Python/Node ports.
 * (The Brood port deliberately uses `d*d > m` instead: there a mixed int/float
 * compare coerces, so the multiply is cheaper than the float bound. Same algorithm,
 * same answer, each written the way that language would write it.)
 *
 * No barrier: the division is data-dependent and the early `return 0` is
 * unpredictable, so there is nothing here for the compiler to close-form. */
#include "bench.h"
#include <math.h>

static int is_prime(int k) {
    if (k < 2) return 0;
    int limit = (int)floor(sqrt((double)k));
    for (int d = 2; d <= limit; d++)
        if (k % d == 0) return 0;
    return 1;
}

int main(void) {
    long n = bench_n(150000);
    long count = 0;
    for (int k = 2; k < (int)n; k++)
        if (is_prime(k)) count++;
    printf("%ld\n", count);
    return 0;
}
