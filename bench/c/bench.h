/* bench.h — shared scaffolding for the C column.
 *
 * The C column exists to give every other row a MACHINE FLOOR to be read against.
 * It is not a full port: C runs the compute rows only (the `all+c` rows in
 * harness.py). The concurrency rows have no honest C answer — 300k held-alive units
 * would be 300k pthread stacks (~2 GB), and a supervisor would be a loop this repo
 * wrote, which measures the harness author. The codec rows would measure whichever
 * third-party C library was picked, since C ships none. Those absences are the same
 * judgement `spawn-live` and `supervisor` already make about their own columns.
 *
 * ---------------------------------------------------------------------------
 * THE ELISION AUDIT — and why this file carries no anti-elision machinery
 *
 * The obvious worry with a C column is that it measures the COMPILER rather than
 * the machine: a C compiler at -O2 is free to replace an algorithm with a closed
 * form, so `loop` (sum 0..n-1) could print the right checksum having never
 * iterated. That would not be "C is fast at iteration", it would be C not running
 * the benchmark, and publishing it would be a fraudulent column.
 *
 * This file originally carried an asm-barrier macro to force iteration. **The
 * barrier was removed after measuring, because the premise was false.** On the
 * compiler in the header (GCC 15.2.0, -O2 -march=native, x86-64):
 *
 *   - `loop` is NOT closed-formed. The asm contains a real back-edge, no SIMD, and
 *     no imul/shr closed-form markers. It runs 30,000,000 real iterations.
 *   - Timings across three builds: -O0 60 ms, -O2 8 ms, -O2-with-barrier 12 ms.
 *     A closed form would have been ~0.4 ms (bare process startup). 8 ms is
 *     ~0.9 cycles/iteration — an unrolled scalar add chain, i.e. the real loop.
 *   - So the barrier was not preventing elision. It was costing 50% by pinning the
 *     accumulator every pass and blocking unrolling — a handicap applied to C on a
 *     false premise, which is exactly the kind of thumb-on-the-scale this suite
 *     is supposed to refuse in either direction.
 *
 * The structural reason elision is not a live risk here: every benchmark prints a
 * checksum derived from the whole computation, and the harness gates on that
 * checksum matching the other six languages. Work that is eliminated cannot
 * produce the checksum. Closed-forming remains theoretically possible on the
 * simplest rows, which is why `loop`'s asm is inspected rather than assumed — see
 * bench/c/README.md for the audit, and re-run it if the compiler changes.
 *
 * The honest summary: C is fast on these rows because it is C, not because it
 * skipped anything.
 * ---------------------------------------------------------------------------
 */
#ifndef BENCH_H
#define BENCH_H

#include <stdio.h>
#include <stdlib.h>

/* Workload size: BENCH_N if set, else the same default every other port bakes in. */
static inline long bench_n(long fallback) {
    const char *e = getenv("BENCH_N");
    if (!e || !*e) return fallback;
    char *end;
    long v = strtol(e, &end, 10);
    return (end == e) ? fallback : v;
}

#endif /* BENCH_H */
