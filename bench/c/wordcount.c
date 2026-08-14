/* Hash-map build. LCG -> key in 0..999, count occurrences, checksum = sum(key*count).
 *
 * READ THIS BEFORE TRUSTING THE NUMBER — this is the row where C's result depends
 * most on the code in this file rather than on C.
 *
 * The keys are `x % 1000`, i.e. dense in 0..999, so the fastest *idiomatic* C here
 * is a flat `long counts[1000]` — an array index, no hashing at all. That would be
 * a perfectly reasonable thing for a C programmer to write, and it would also not
 * be this benchmark: every other column builds a real hash map, and the row is
 * named "hash-map build". An array would report C as infinitely fast at a data
 * structure it never constructed.
 *
 * So this uses a hand-written open-addressing table with linear probing, which is
 * what C reaches for when there is no dense key range — C has no stdlib hash map.
 * The consequence to keep in mind: this table is simpler than the production hash
 * maps the other runtimes ship (no resizing policy beyond power-of-two growth, no
 * SIMD probing, integer keys only), so it is fast partly because it does less. Read
 * this row as "a straightforward C hash table", not as "the C hash map". */
#include "bench.h"

#define EMPTY (-1)

typedef struct {
    long *keys;
    long *vals;
    size_t mask;
} Table;

static void table_init(Table *t, size_t cap_pow2) {
    t->keys = malloc(cap_pow2 * sizeof *t->keys);
    t->vals = calloc(cap_pow2, sizeof *t->vals);
    t->mask = cap_pow2 - 1;
    for (size_t i = 0; i < cap_pow2; i++) t->keys[i] = EMPTY;
}

/* Fibonacci hashing — cheap and adequate for integer keys. */
static inline size_t slot(const Table *t, long key) {
    return (size_t)((unsigned long)key * 11400714819323198485UL) & t->mask;
}

static void table_bump(Table *t, long key) {
    size_t i = slot(t, key);
    for (;;) {
        if (t->keys[i] == key) { t->vals[i]++; return; }
        if (t->keys[i] == EMPTY) { t->keys[i] = key; t->vals[i] = 1; return; }
        i = (i + 1) & t->mask;
    }
}

int main(void) {
    long n = bench_n(750000);
    const long K = 1000;

    Table t;
    table_init(&t, 4096); /* > 2x the 1000 distinct keys, so load factor stays low */

    long x = 123456789;
    for (long i = 0; i < n; i++) {
        x = (x * 1103515245 + 12345) & 0x7FFFFFFF;
        table_bump(&t, x % K);
    }

    long total = 0;
    for (size_t i = 0; i <= t.mask; i++)
        if (t.keys[i] != EMPTY) total += t.keys[i] * t.vals[i];

    printf("%ld\n", total);
    free(t.keys);
    free(t.vals);
    return 0;
}
