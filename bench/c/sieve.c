/* Sieve of Eratosthenes to n. Checksum = count of primes <= n.
 *
 * A flat byte array, which is what every port uses here (the row is explicitly
 * "mutable array vs Table" — it is where Brood's persistent structures are
 * measured against raw mutable memory, so C using raw mutable memory is the whole
 * point of the comparison).
 *
 * `char` rather than a bitset: the other columns all use a byte-per-entry array or
 * equivalent, and a bitset would be a different space/time tradeoff than they made.
 *
 * No barrier: the count depends on the sieved array. */
#include "bench.h"
#include <string.h>

int main(void) {
    long n = bench_n(1000000);

    char *comp = calloc((size_t)n + 1, 1);
    if (!comp) return 1;

    for (long p = 2; p * p <= n; p++)
        if (!comp[p])
            for (long j = p * p; j <= n; j += p) comp[j] = 1;

    long count = 0;
    for (long k = 2; k <= n; k++) if (!comp[k]) count++;

    printf("%ld\n", count);
    free(comp);
    return 0;
}
