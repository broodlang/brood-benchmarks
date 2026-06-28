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
language on that row. Two of the old headline gaps have closed sharply: `nqueens` and `bintree` are
down from ~29× / ~20× to ~6–7× as JIT coverage widened, so the largest gaps are now elsewhere:

- **`matmul` (~17× — but noise-sensitive; .NET is only ~5 ms)** — the inner loop is native, so the
  91 ms absolute is respectable; the ratio is inflated by .NET's tiny denominator. The residual is
  the one read LICM can't hoist (the per-`k` row) plus the boxed 24-byte `Value` vs a register `long`.
- **`wordcount` (~13×)** — *not* an immutability cost: both Clojure (313 ms) and Elixir (182 ms) use
  immutable persistent maps and beat Brood (410 ms — Clojure now edges ahead on a fair core pin), so
  the gap is Brood's young CHAMP map's constant factors (two trie walks per update — no single-pass
  `map-update` primitive yet — plus per-level path-copy allocation), not the persistent approach.
- **`mandelbrot` (~11×)** — float-comparison loop *is* JIT'd, yet 238 ms vs .NET's 21 ms: the residual
  is boxed `f64` values and the escape-count inner body the JIT doesn't fully lower. A real gap, not a
  ratio artefact.
- **`pipeline` (~7×), `nqueens` (~6.7×), `bintree` (~6.2×)** — backtracking + short-lived allocation
  (lazy-seq cells, per-step list/tree building) the JIT doesn't cover; allocation/GC churn dominates.
- **`sort` (~2.6×), `primes` (~3.2×), `loop` (~3.0×)** — Brood's closest compute gaps; mostly raw
  dispatch overhead.

`errors-deep` is a reminder that a compute-loop-only view misleads: .NET tops the arithmetic rows
yet is *worst* at deep error recovery (stack-trace capture per throw). It's an axis where Brood is
already competitive, not a gap to close.

## Candidate levers (rough priority)

1. **The immutable map build** (`wordcount`, ~13×, 410 ms) — now Brood's largest *absolute* compute
   gap. A single-pass `map-update` primitive (one trie walk per update instead of two) and cheaper
   CHAMP path-copy. The immutable-Lisp peers (Clojure, Elixir) prove the approach isn't the problem.
2. **Float lowering** (`mandelbrot`, ~11×, 238 ms) — the float loop already JITs, but values stay
   boxed `f64`; keeping them in registers through the escape-count body is the lever here.
3. **Heap-walking / allocation-heavy code** (`bintree`, `nqueens`, `pipeline`, now ~6–7×, down from
   ~20–29×) — much improved as JIT coverage widened, but the structure-walkers still don't tier and
   their heap reads go through per-op FFI callbacks. Tiering them + inlining heap reads
   (`ptr + idx*stride`, already proven for the hoisted array case) is the remaining win toward Elixir.
4. **True call inlining / bounded unroll** — removes calls rather than cheapening them; the remaining
   `fib`-class lever (~5.7×) after the in-IR fast-link. (Note: a measured attempt to push the
   *dispatch* lever further — moving the call frame-setup fully into JIT IR — regressed and was
   reverted; the FFI boundary is not the bottleneck. See the Brood repo devlog, 2026-06-19.)
5. **Interpreter dispatch** — the ~60 % `vm_run_bc` share bounds every un-JIT'd row.

See [`results/report.md`](results/report.md) for the current numbers and
[`results/positioning.svg`](results/positioning.svg) for the compute-vs-memory map.
