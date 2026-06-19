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
caller links straight to a JIT'd callee through an epoch-guarded, in-IR call-site fast-link, which
took `fib` compute from ~502 → ~274 ms (~11× → ~7× off the fastest). A `def` deopts affected code, so
Emacs-style hot reload holds. Workers in `spawn`/`pfib` share one compiled copy of the native code
instead of each recompiling.

Still interpreted (the weak rows; ratios vs the fastest language) — these bail the JIT:

- **`nqueens` (~29×), `bintree` (~20×)** — backtracking + short-lived allocation the JIT doesn't
  cover; the per-step list/tree building dominates.
- **`wordcount` (~18×)** — *not* an immutability cost: both Clojure (528 ms) and Elixir use immutable
  persistent maps and beat Brood (810 ms), so the gap is Brood's young CHAMP map's constant factors
  (two trie walks per update — no single-pass `map-update` primitive yet — plus per-level path-copy
  allocation), not the persistent approach. The two immutable-Lisp peers are the proof.
- **`matmul` (~24× — noise-sensitive on .NET's ~6 ms)** — the inner loop is native; the residual is
  the one read LICM can't hoist (the per-`k` row) plus the boxed 24-byte `Value` vs a register `long`.
- **`sort` (~3.7×), `primes` (~5×)** — Brood's closest compute gaps; mostly raw dispatch overhead.

`errors-deep` is a reminder that a compute-loop-only view misleads: .NET tops the arithmetic rows
yet is *worst* at deep error recovery (stack-trace capture per throw). It's an axis where Brood is
already competitive, not a gap to close.

## Candidate levers (rough priority)

1. **Heap-walking / allocation-heavy code** (`bintree`, `nqueens`) — the largest gaps. The
   structure-walkers don't tier and their heap reads go through per-op FFI callbacks (no faster than
   the VM). Tiering them + inlining heap reads (`ptr + idx*stride`, already proven for the hoisted
   array case) is the biggest available win and the widest gap to Elixir.
2. **The immutable map build** (`wordcount`) — a single-pass `map-update` primitive and cheaper
   CHAMP path-copy.
3. **True call inlining / bounded unroll** — removes calls rather than cheapening them; the remaining
   `fib`-class lever after the in-IR fast-link. (Note: a measured attempt to push the *dispatch*
   lever further — moving the call frame-setup fully into JIT IR — regressed and was reverted; the
   FFI boundary is not the bottleneck. See the Brood repo devlog, 2026-06-19.)
4. **Interpreter dispatch** — the ~60 % `vm_run_bc` share bounds every un-JIT'd row.

See [`results/report.md`](results/report.md) for the current numbers and
[`results/positioning.svg`](results/positioning.svg) for the compute-vs-memory map.
