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
with no alias analysis because Brood data is immutable), **non-tail recursion** (`fib`), and
**inline small-vector reads** (`(nth v <const>)` on a LOCAL vector, the analog of the pair
`first`/`rest` inline — `bintree`). A JIT'd caller links straight to a JIT'd callee through an
epoch-guarded, in-IR call-site fast-link; `fib` compute is now ~225 ms, ~5.7× off the fastest (down
from ~502 ms before the fast-link). A `def` deopts affected code, so Emacs-style hot reload holds.
Workers in `spawn`/`pfib` share one compiled copy of the native code instead of each recompiling.

Still interpreted (or only partly JIT'd) — the weak rows; ratios are Brood's compute vs the fastest
language on that row. Several old headline gaps have closed or inverted:

- **`matmul` (~23× — .NET is only ~4 ms)** — the inner loop is native, so the ~95 ms absolute is
  respectable; the ratio is inflated by .NET's tiny denominator. The residual is the one read LICM
  can't hoist (the per-`k` row) plus the boxed 24-byte `Value` vs a register `long`.
- **`bintree` (~6.1×)** — **closed from ~6.7× / 6th → 4th (98 ms → 85 ms)** by inline small-vector
  storage (2026-07-01): a small vector's elements live **inline in its slab slot** (not a separately
  `malloc`'d `Vec`), so a 2-element node allocates as a bump-push (like a `cons`), and the JIT inlines
  the `(nth node 0/1)` reads. Brood now beats Python (96 ms) and Ruby (98 ms); .NET/Elixir (~14 ms)
  stay ahead. Remaining headroom is the non-tail-call safepoints in `check`/`make` that block the
  in-arm alloc inline.
- **`nqueens` (~14×)** — backtracking recursion; the `reduce`-over-`range` per node and the
  non-tail `solve`/`safe?` recursion dominate (pair `first`/`rest` in `safe?` already inline). Node
  (~7 ms) and Elixir (~12 ms) lead.
- **`mandelbrot` (~11×)** — `esc` *is* JIT'd **and** its `f64` loop params are already
  register-carried (native `fadd`/`fmul`, block-param phis; verified via CLIF), yet 212 ms
  vs .NET's 19 ms. The residual is the boxed 24-byte `Value` tagging *in the arithmetic
  itself* (tag-check + box/unbox around each op) plus per-iteration loop overhead — **not**
  the frame stores: eliding the back-edge slot stores was prototyped and gave ~0 (they're
  absorbed by the CPU store buffer). See the Brood repo devlog (2026-07-01, "store-elision").
  `mandelbrot` is near the current JIT floor.
- **`pipeline` (~7×)** — lazy-seq and filter/map/reduce composition the JIT doesn't cover;
  allocation churn dominates.
- **`wordcount` (~3.5×)** — **closed from ~13× in an earlier run** by the LINMAP compile-time
  pass (2026-06-28): self-tail-recursive integer-count accumulators are detected and rewritten to
  use a mutable Table internally (`map-int-add → table-incr`), avoiding the CHAMP path-copy on
  every step. Brood (109 ms) now beats Elixir (177 ms) and Python (169 ms) here; Node and .NET stay
  ahead with mutable hash maps (~31–40 ms).
- **`sort` (~2.3×)** — the numeric `(sort nums)` already uses the native `%sort-asc`, so the
  benchmark's cost is **building** the input list, which was GC-bound: the collector re-copied the
  growing all-live accumulator. Cut 173→156 ms (2026-07-01) by scaling the nursery threshold with
  *total* live (young+old, not young-only — a tenuring build left young ≈ 0 and collapsed it to the
  floor) and making majors on an all-live old gen rarer. General to any large list/sequence build.
- **`primes` (~4×), `loop` (~3.3×)** — Brood's closest compute gaps; mostly raw dispatch overhead.

`errors-deep` is a reminder that a compute-loop-only view misleads: .NET tops the arithmetic rows
yet is *worst* at deep error recovery (stack-trace capture per throw, ~672 ms). Elixir (OTP 28) is
fastest there (~10 ms for 50k throws). It's an axis where Brood is already 2nd.

- **`pfib` (~7.3× — the parallel-native scaling row)** — two JIT parallel-scaling fixes landed
  2026-07-02 (Brood repo devlog), and this row's **N was bumped 28 → 31** so it actually exercises
  parallel-native *scaling* rather than task startup/teardown (at N=28 even .NET spent only ~33 ms of
  compute, below the suite's ~100 ms floor). (1) The two-stage-tiering *inlined-upgrade* swap used
  the **shared** global epoch to re-point its own call sites, which invalidated every peer green
  process's arm too → a cross-process re-tier/re-swap/re-bump cascade that pushed nearly every call
  onto the slow IC-dispatch path (~2–3× the instructions); the swap now invalidates only the swapping
  process's fast-links to that callee. (2) The *inlined* native (the recursive self-inline, ~1.7× on
  `fib`) was compiled **per-process**, so for a short fan-out most workers finished before their own
  deferred compile landed and never got the inline win; it's now **shared across processes** via a
  companion cache (`RuntimeCode::jit_inline_cache`) exactly as the small native already was — one
  inlined compile serves every worker (this is how the BEAM/BeamAsm shares module native code). At
  N=32 the two together took the 100-way fan-out **337B→~119B instructions and 4.7s→1.42s (~3.3×)**.
  The gap to .NET on this row narrowed from ~12× (warmup-dominated N=28) to **~7.3×** at N=31, where
  the run is real steady-state parallel compute. Remaining headroom is `fib`'s own single-thread gap
  (~5.7×, the true call-inlining lever below) plus green-scheduler/coroutine overhead vs OS threads.

## Candidate levers (rough priority)

1. ~~**Float lowering** (`mandelbrot`)~~ — **closed / dead end.** `esc`'s floats are already
   register-carried; the residual is `Value` tagging in the arithmetic, not stores. Eliding
   the back-edge stores was tried (2026-07-01) and gave ~0 — the stores are free (store
   buffer). Don't re-attempt. `mandelbrot` is near the JIT floor.
2. **Heap-walking / allocation-heavy code** (`nqueens`, `pipeline`, ~7–14×) — the structure-walkers
   still don't tier and some heap reads go through per-op FFI callbacks. The inline small-vector
   storage + read (2026-07-01, which closed `bintree`) is the proven template; extending it to
   variable-index reads and to in-arm alloc (blocked today by non-tail-call safepoints) is the
   remaining win toward Elixir. `nqueens` also wants the `reduce`-over-`range` per node cheaper.
3. **`matmul`** (~25× ratio, but .NET is only 4 ms so it's noise-sensitive; 100 ms absolute is not
   a priority) — the ratio is inflated by .NET's tiny denominator more than by any Brood weakness.
4. **True call inlining / bounded unroll** — removes calls rather than cheapening them; the remaining
   `fib`-class lever (~5.7×) after the in-IR fast-link. (Note: a measured attempt to push the
   *dispatch* lever further — moving the call frame-setup fully into JIT IR — regressed and was
   reverted; the FFI boundary is not the bottleneck. See the Brood repo devlog, 2026-06-19.)
5. **Interpreter dispatch** — the ~60 % `vm_run_bc` share bounds every un-JIT'd row.
6. **LINMAP wider coverage** (`wordcount` is now closed; the next target is `reduce`-style folds
   over non-integer values — requires extending the Table to hold non-serialisable `Value`s, or a
   type-directed variant that falls back gracefully).

See [`results/report.md`](results/report.md) for the current numbers and
[`results/positioning.svg`](results/positioning.svg) for the compute-vs-memory map.
