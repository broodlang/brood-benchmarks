/* Sort n LCG-generated longs, then a checksum walk. Checksum = fold h*31+v mod 1e9+7.
 *
 * Uses `qsort`, which is C's standard sort. Worth knowing when reading the number:
 * qsort takes its comparator as a function POINTER and calls it indirectly per
 * comparison, so C does not get the inlined-comparator advantage that C++
 * `std::sort` or a monomorphised generic sort would give it. That is a real
 * property of the C standard library, not a handicap applied here — and it is the
 * closest analogue to the other columns, which also call a comparison through a
 * runtime value.
 *
 * No barrier: the checksum depends on the sorted order of unpredictable data. */
#include "bench.h"

static int cmp_long(const void *a, const void *b) {
    long x = *(const long *)a, y = *(const long *)b;
    return (x > y) - (x < y);
}

int main(void) {
    long n = bench_n(375000);
    const long MOD = 1000000007;

    long *data = malloc((size_t)n * sizeof *data);
    if (!data) return 1;

    long x = 123456789;
    for (long i = 0; i < n; i++) {
        x = (x * 1103515245 + 12345) & 0x7FFFFFFF;
        data[i] = x;
    }

    qsort(data, (size_t)n, sizeof *data, cmp_long);

    long h = 0;
    for (long i = 0; i < n; i++) h = (h * 31 + data[i]) % MOD;

    printf("%ld\n", h);
    free(data);
    return 0;
}
