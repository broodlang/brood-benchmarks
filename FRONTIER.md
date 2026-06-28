# Optimization frontier — where the gaps are and what would move them

Core-dev notes: the *interpretation* of the [benchmark data](BENCHMARKS.md). This is where
implementation suggestions live — the [README](README.md) stays a plain "where we stand" for
everyone else. Upstream, the canonical version is the Brood repo's `docs/compute-frontier.md`; this
file is the benchmark-suite-local read.

None of the gaps below are architectural — they are implementation headroom in a young runtime.
Profiling puts ~60 % of an interpreted benchmark's time in the bytecode dispatch loop (`vm_run_bc`),
so the two broad levers are **interpreter-dispatch cost** and **widening JIT coverage**.

## What runs native vs interpreted

The tier-1 JIT covers: integer self-tail loops (`loop`, `collatz`), float-comparison loops
(`mandelbrot`), indexed array reads (`matmul`'s inner `dot`, via loop-invariant hoisting — sound
with no alias analysis because Brood data is immutable), and **non-tail recursion** (`fib`). A JIT'd
caller links straight to a JIT'd callee through an epoch-guarded, in-IR call-site fast-link; `fib`
compute is now ~242 ms, ~5.7× off the fastest (down from ~502 ms before the fast-link). A `def`
deopts affected code, so Emacs-style hot reload holds. Workers in `spawn`/`pfib` share one compiled
copy of the native code instead of each recompiling.

Still interpreted (or only partly JIT'd) — the weak rows; ratios are Brood's compute vs the fastest
language on that row. Several old headline gaps have closed or inverted:

- **`matmul` (~25× — .NET is only ~4 ms)** — the inner loop is native, so the 100 ms absolute is
  respectable; the ratio is inflated by .NET's tiny denominator. The residual is the one read LICM
  can't hoist (the per-`k` row) plus the boxed 24-byte `Value` vs a register `long`.
- **`bintree` (~16×)** and **`nqueens` (~13×)** — Elixir (OTP 28) sharpened these (7 ms each, vs
  ~18 ms and ~14 ms before); Brood's structure-walkers are still fully interpreted. Down from ~6× /
  ~7× in real terms on Brood's side, but the denominator shrank.
- **`mandelbrot` (~12×)** — float-comparison loop *is* JIT'd, yet 235 ms vs .NET's 20 ms: the
  residual is boxed `f64` values and the escape-count inner body the JIT doesn't fully lower.
- **`pipeline` (~9×)** — lazy-seq and filter/map/reduce composition the JIT doesn't cover;
  allocation churn dominates.
- **`wordcount` (~3.7×)** — **closed from ~13× in the previous run** by the LINMAP compile-time
  pass (2026-06-28): self-tail-recursive integer-count accumulators are detected and rewritten to
  use a mutable Table internally (`map-int-add → table-incr`), avoiding the CHAMP path-copy on
  every step. Brood (118 ms) now beats Elixir (167 ms) here; Node and .NET stay ahead with mutable
  hash maps (~32–39 ms).
- **`sort` (~2.7×), `primes` (~4×), `loop` (~3.0×)** — Brood's closest compute gaps; mostly raw
  dispatch overhead.

`errors-deep` is a reminder that a compute-loop-only view misleads: .NET tops the arithmetic rows
yet is *worst* at deep error recovery (stack-trace capture per throw, ~782 ms). Elixir (OTP 28) is
now effectively free there (<1 ms for 50k throws). It's an axis where Brood is already 2nd.

## Candidate levers (rough priority)

1. **Float lowering** (`mandelbrot`, ~12×, 235 ms) — the float loop already JITs, but values stay
   boxed `f64`; keeping them in registers through the escape-count body is the lever here.
2. **Heap-walking / allocation-heavy code** (`bintree`, `nqueens`, `pipeline`, ~9–16×) — the
   structure-walkers still don't tier and their heap reads go through per-op FFI callbacks. Tiering
   them + inlining heap reads (`ptr + idx*stride`, already proven for the hoisted array case) is the
   remaining win toward Elixir.
3. **`matmul`** (~25× ratio, but .NET is only 4 ms so it's noise-sensitive; 100 ms absolute is not
   a priority) — the ratio is inflated by .NET's tiny denominator more than by any Brood weakness.
4. **True call inlining / bounded unroll** — removes calls rather than cheapening them; the remaining
   `fib`-class lever (~5.8×) after the in-IR fast-link. (Note: a measured attempt to push the
   *dispatch* lever further — moving the call frame-setup fully into JIT IR — regressed and was
   reverted; the FFI boundary is not the bottleneck. See the Brood repo devlog, 2026-06-19.)
5. **Interpreter dispatch** — the ~60 % `vm_run_bc` share bounds every un-JIT'd row.
6. **LINMAP wider coverage** (`wordcount` is now closed; the next target is `reduce`-style folds
   over non-integer values — requires extending the Table to hold non-serialisable `Value`s, or a
   type-directed variant that falls back gracefully).

See [`results/report.md`](results/report.md) for the current numbers and
[`results/positioning.svg`](results/positioning.svg) for the compute-vs-memory map.
