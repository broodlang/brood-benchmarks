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
epoch-guarded, in-IR call-site fast-link. For int-only single-arg recursion (`fib`) an **unboxed-`i64`
register calling convention** (2026-07-02) drops the boxing + roots-staging + fast-link dispatch at the
recursive call boundary entirely — args/results ride in registers, overflow-checked with a deopt to the
VM (BigInt) on overflow — taking `fib` compute **227 → 54 ms (5th → 2nd, beating Elixir)**. A `def`
deopts affected code, so Emacs-style hot reload holds.
Workers in `spawn`/`pfib` share one compiled copy of the native code instead of each recompiling.

Still interpreted (or only partly JIT'd) — the weak rows; ratios are Brood's compute vs the fastest
language on that row. Several old headline gaps have closed or inverted:

- **`matmul` (~7× — .NET is ~26 ms) — regressed 94 → 204 ms, now mostly fixed at ~165 ms.** The inner
  loop is native, and the residual has always been the one read LICM can't hoist (the per-`k` row) plus
  the boxed 24-byte `Value` vs a register `long`. The doubling to 204 ms was root-caused (bisect →
  ADR-091): its `def`'d matrices live in the shared RUNTIME region, and multigen made every RUNTIME-handle
  deref pay an `ArcSwap::load` (~13.6 % of runtime, ~16 M reads). Fixed by a per-process generation-pin
  cache (brood `c3b55dd`) that clones a cached `Arc` gated on a version counter instead of loading the
  ArcSwap per deref. The remaining gap vs 94 ms is the per-deref `Arc` clone (kept for robust pinning)
  plus the LICM/boxing residual above.
- **`bintree` (~9.6× — Elixir's BEAM is unusually fast here at ~10 ms)** — **closed 6th → 4th
  (98 ms → 90 ms)** by inline small-vector
  storage (2026-07-01): a small vector's elements live **inline in its slab slot** (not a separately
  `malloc`'d `Vec`), so a 2-element node allocates as a bump-push (like a `cons`), and the JIT inlines
  the `(nth node 0/1)` reads. Brood now beats Python (94 ms) and Ruby (97 ms); Elixir (~10 ms) and
  .NET (~16 ms) stay ahead. Remaining headroom is the non-tail-call safepoints in `check`/`make` that
  block the in-arm alloc inline.
- **`nqueens` (~11×)** — backtracking recursion; the `reduce`-over-`range` per node and the
  non-tail `solve`/`safe?` recursion dominate (pair `first`/`rest` in `safe?` already inline). Node
  (~8 ms) and Elixir (~20 ms) lead.
- **`mandelbrot` (~10×)** — `esc` *is* JIT'd **and** its `f64` loop params are already
  register-carried (native `fadd`/`fmul`, block-param phis; verified via CLIF), yet 217 ms
  vs .NET's 21 ms. The residual is the boxed 24-byte `Value` tagging *in the arithmetic
  itself* (tag-check + box/unbox around each op) plus per-iteration loop overhead — **not**
  the frame stores: eliding the back-edge slot stores was prototyped and gave ~0 (they're
  absorbed by the CPU store buffer). See the Brood repo devlog (2026-07-01, "store-elision").
  `mandelbrot` is near the current JIT floor.
- **`pipeline` (~8×)** — lazy-seq and filter/map/reduce composition the JIT doesn't cover;
  allocation churn dominates.
- **`wordcount` (~3.7×)** — **closed from ~13× in an earlier run** by the LINMAP compile-time
  pass (2026-06-28): self-tail-recursive integer-count accumulators are detected and rewritten to
  use a mutable Table internally (`map-int-add → table-incr`), avoiding the CHAMP path-copy on
  every step. Brood (114 ms) now beats Elixir (150 ms) and Python (175 ms) here; Node and .NET stay
  ahead with mutable hash maps (~32–38 ms).
- **`sort` (~2.4×)** — the numeric `(sort nums)` already uses the native `%sort-asc`, so the
  benchmark's cost is **building** the input list, which was GC-bound: the collector re-copied the
  growing all-live accumulator. Cut 173→156 ms (2026-07-01) by scaling the nursery threshold with
  *total* live (young+old, not young-only — a tenuring build left young ≈ 0 and collapsed it to the
  floor) and making majors on an all-live old gen rarer. General to any large list/sequence build.
- **`primes` (~4.5×), `loop` (~2.9×)** — Brood's closest compute gaps; mostly raw dispatch overhead.

`errors-deep` is a reminder that a compute-loop-only view misleads: .NET tops the arithmetic rows
yet is *worst* at deep error recovery (stack-trace capture per throw, ~710 ms). Elixir (OTP 28) is
fastest there (its 50k-throw compute falls below its own boot noise). It's an axis where Brood is already 2nd.

- **`pfib` (~1.5× — 2nd, beating Elixir)** — three wins landed 2026-07-02 (Brood repo devlog). First
  the N was bumped 28 → 31 so the row exercises parallel-native *scaling* not task startup/teardown.
  Then two JIT fixes: (1) the two-stage-tiering inlined-upgrade swap used the **shared** global epoch,
  invalidating every peer green process's arm → a cross-process re-tier cascade onto the slow
  IC-dispatch path; the swap now invalidates only the swapping process's fast-links. (2) The inlined
  native was compiled **per-process**; it's now **shared across processes** (one compile serves every
  worker, like the BEAM). Finally the **unboxed-`i64` calling convention** (see `fib` above) removed
  the recursive-call boxing: `pfib` went **847 → 168 ms**, from 5th to **2nd (1.5× off .NET)**, ahead
  of Elixir (297 ms) and Node (301 ms). Parallel scaling itself is already ~93% of the machine's
  OS-process ceiling (Brood green 3.93× vs 4.20× for independent OS processes on this 12-core box —
  it even beats Elixir's 3.30×), so the residual is just `fib`'s single-thread gap (now ~1.5×).

## Wider-range findings (2026-07-12)

Nine benchmarks widened coverage past the numeric/allocation core; they surfaced several concrete
targets, ranked here by value. None are in the positioning-chart aggregate (that stays the original
core-compute rows) — they are reported on their own precisely because they are library/representation
gaps, not core VM speed.

1. **Message-passing latency — `pingpong` is ~14× behind the BEAM (highest-value new target).**
   Brood does a send+receive round-trip in ~6.6 µs (663 ms / 100 k) vs Elixir's ~0.47 µs (47 ms);
   `ring` echoes it (Brood 2.2 s vs Elixir 262 ms). This is Brood's *home turf* — Erlang-style
   isolated processes — and it is nowhere near BEAM parity on raw mailbox latency. Suspects: the
   `receive` selective-scan cost, mailbox locking, and scheduler wake-up/hand-off latency on a
   two-process ping-pong. Brood already beats the real-thread languages (Python/Ruby/Clojure, 3.6–4.9 s
   on `ring`), so the gap is specifically vs a tuned actor scheduler. This is the most important
   lever the wider range exposed.
2. **`std/json` is super-linear and `std/encoding` (base64) blows RSS — pure-Brood library bugs.**
   `json` encode+parse is ~O(n²) (2 000 recs → 2.5 s, 5 000 → 12.7 s); `base64` peaks at **1.3 GB
   RSS** at 50 k bytes. These are Brood-source fixes (quadratic string building in the encoders; an
   intermediate-list blow-up in base64), not VM work — the cheapest wins on the board, and exactly
   the kind of gap dogfooding is meant to catch. `regex` is merely linear-but-interpreted (pure-Brood
   backtracking that re-parses the pattern each `matches?`), a smaller structural cost.
3. **Immutable numeric loops — `nbody` ~850×.** Rebuilding immutable body vectors every step
   dominates; there is no lever here without either escape analysis that stack-allocates/reuses the
   per-step vectors or a native float-array primitive (philosophically fraught — see the mutable-data
   invariant). Likely stays a known immutable-cost data point rather than a target.
4. **Non-tail deep recursion — `ackermann` ~16×.** Brood's `ack(3,9)` (depth ~4093, non-tail double
   recursion) runs 4.1 s, near Python — the JIT covers `fib`'s non-tail *single* recursion but not
   this `cond` + double-recursion shape, so it interprets. Extending the non-tail-recursion JIT
   coverage is the lever; distinct from `fib`, which already tiers.
5. **`sieve` ~316× and `persistent-map` ~30×** — the expected cost of the immutable model: a `Table`
   (ETS) standing in for a mutable bool array, and CHAMP path-copy under read-modify-write. Known
   costs, not bugs; a bitset primitive would help `sieve` but adds a builtin.

## Candidate levers (rough priority)

1. ~~**Float lowering** (`mandelbrot`)~~ — **closed / dead end.** `esc`'s floats are already
   register-carried; the residual is `Value` tagging in the arithmetic, not stores. Eliding
   the back-edge stores was tried (2026-07-01) and gave ~0 — the stores are free (store
   buffer). Don't re-attempt. `mandelbrot` is near the JIT floor.
2. **Heap-walking / allocation-heavy code** (`nqueens`, `pipeline`, ~8–11×) — the structure-walkers
   still don't tier and some heap reads go through per-op FFI callbacks. The inline small-vector
   storage + read (2026-07-01, which closed `bintree`) is the proven template; extending it to
   variable-index reads and to in-arm alloc (blocked today by non-tail-call safepoints) is the
   remaining win toward Elixir. `nqueens` also wants the `reduce`-over-`range` per node cheaper.
3. **`matmul`** (~19× ratio, but .NET is only 5 ms so it's noise-sensitive; 94 ms absolute is not
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
