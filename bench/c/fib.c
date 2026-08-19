/* Naive recursion / function-call overhead. fib(35), checksum = 9227465.
 *
 * No barrier needed and none used: `n` is a runtime value, the recursion is not
 * memoisable by the compiler, and GCC does not close-form Fibonacci. The two
 * recursive calls are real calls (GCC partially inlines the shallow ones, exactly
 * as every JIT here does). Verified against -O0 in bench/c/README.md. */
#include "bench.h"

static long fib(long n) {
    return n < 2 ? n : fib(n - 1) + fib(n - 2);
}

int main(void) {
    long n = bench_n(35);
    printf("%ld\n", fib(n));
    return 0;
}
