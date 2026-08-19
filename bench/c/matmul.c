/* Nested loops + indexing (integer NxN). Checksum = total % 1000000007.
 *
 * Row-of-pointers layout (int **), matching the jagged `int[n][]` every other port
 * uses — NOT a flat contiguous block. That is deliberate: a flat array would let C
 * vectorise the inner product in a way none of the other ports can, and the row is
 * about indexed access through the language's ordinary 2-D representation. The
 * pointer chase per row is exactly what Brood/Elixir/C# pay.
 *
 * No barrier: the accumulation is over loaded memory the compiler cannot predict. */
#include "bench.h"

int main(void) {
    long n = bench_n(175);
    const long MOD = 1000000007;

    int **a = malloc((size_t)n * sizeof *a);
    int **b = malloc((size_t)n * sizeof *b);
    if (!a || !b) return 1;
    for (long i = 0; i < n; i++) {
        a[i] = malloc((size_t)n * sizeof *a[i]);
        b[i] = malloc((size_t)n * sizeof *b[i]);
        if (!a[i] || !b[i]) return 1;
        for (long j = 0; j < n; j++) {
            a[i][j] = (int)((i + j) % 100);
            b[i][j] = (int)((i * j) % 100);
        }
    }

    long total = 0;
    for (long i = 0; i < n; i++) {
        const int *ai = a[i];
        for (long j = 0; j < n; j++) {
            long s = 0;
            for (long k = 0; k < n; k++) s += (long)ai[k] * b[k][j];
            total += s;
        }
    }
    printf("%ld\n", total % MOD);
    return 0;
}
