/* Higher-order fold over a range. Checksum = sum 0..n-1, same as `loop`.
 *
 * The row measures applying a FUNCTION VALUE per element — Clojure's `reduce`,
 * Elixir's `Enum.reduce`, .NET's `Aggregate`, Brood's `fold`. It is deliberately
 * distinct from `loop`, the hand-written form.
 *
 * THE CALLBACK IS LEFT STATICALLY KNOWN, so GCC inlines it. That is a deliberate
 * call and it needs stating, because it decides the number.
 *
 * The alternative was to hide the reducer behind an opaque pointer so C had to make
 * a real indirect call per element (measured: 7 ms against 4 ms inlined, ~1.3 ns
 * per call). That was rejected: it holds C to a stricter standard than the rest of
 * the field. Brood specialises a passthrough reducer like `+` into a native counted
 * loop and resolves it ONCE rather than per element (see FRONTIER.md), and V8
 * inlines a monomorphic callback the same way. Forcing C alone to defeat its own
 * inliner would have measured a restriction this harness invented, not the language
 * — the same error as the `loop` barrier that was removed after measuring.
 *
 * So read this row as: what does each language actually do when handed a fold with
 * a known reducer? Brood, Node and C all specialise it away; Python, Ruby and
 * Clojure pay a real call per element. That difference IS the result. If you want
 * C's cost with an unspecialisable callback, it is the 7 ms figure above — recorded
 * in bench/c/README.md so it is not lost. */
#include "bench.h"

static long add(long a, long b) { return a + b; }

static long fold(long (*f)(long, long), long init, long n) {
    long acc = init;
    for (long i = 0; i < n; i++) acc = f(acc, i);
    return acc;
}

int main(void) {
    long n = bench_n(5000000);
    printf("%ld\n", fold(add, 0, n));
    return 0;
}
