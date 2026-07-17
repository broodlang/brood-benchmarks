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

- **`matmul` (135 ms; the ~27× ratio is inflated by .NET's ~5 ms denominator)** — the inner loop is
  native; the residual is the one read LICM can't hoist (the per-`k` row) plus the boxed 24-byte
  `Value` vs a register `long`. A past 94 → 204 ms regression (multigen making every RUNTIME-handle
  deref pay an `ArcSwap::load`, ~13.6 % of runtime) was fixed by a per-process generation-pin cache
  (brood `c3b55dd`); the residual vs 94 ms is the per-deref `Arc` clone kept for robust pinning.
- **`bintree` (115 ms, 6th — Elixir's BEAM is unusually fast here at ~14 ms)** — inline small-vector
  storage (2026-07-01) had closed it to 90 ms / 4th (a 2-element node allocates as a bump-push and
  the JIT inlines the `(nth node 0/1)` reads), but the 2026-07-17 run drifted back to 115 ms, behind
  Python (105 ms) and Ruby (94 ms) again — **unexplained; the current watch-item.** Remaining known
  headroom is the non-tail-call safepoints in `check`/`make` that block the in-arm alloc inline.
- **`nqueens` (80 ms, ~13×)** — backtracking recursion; the `reduce`-over-`range` per node and the
  non-tail `solve`/`safe?` recursion dominate (pair `first`/`rest` in `safe?` already inline). Node
  (~6 ms) and Elixir (~10 ms) lead.
- **`mandelbrot` (174 ms, ~10×)** — `esc` *is* JIT'd **and** its `f64` loop params are already
  register-carried (native `fadd`/`fmul`, block-param phis; verified via CLIF), yet ~10× .NET's
  18 ms. The residual is the boxed 24-byte `Value` tagging *in the arithmetic itself* (tag-check +
  box/unbox around each op) plus per-iteration loop overhead — **not** the frame stores: eliding the
  back-edge slot stores was prototyped and gave ~0 (absorbed by the CPU store buffer; Brood repo
  devlog 2026-07-01). Near the current JIT floor.
- **`pipeline` (30 ms, ~7×)** — lazy-seq and filter/map/reduce composition the JIT doesn't cover;
  allocation churn dominates.
- **`wordcount` (35 ms, 1.1× of Node — 2nd)** — **closed from ~13×** by the LINMAP compile-time pass
  (2026-06-28: self-tail-recursive integer-count accumulators rewritten to a mutable Table
  internally, `map-int-add → table-incr`), then the dense-Table + call-path round. Effectively
  competitive with the mutable-hash languages now.
- **`sort` (205 ms, ~3.3×)** — the numeric `(sort nums)` already uses the native `%sort-asc`, so the
  cost is **building** the input list, which was GC-bound; the nursery threshold now scales with
  *total* live (2026-07-01), general to any large list build. Ruby (70 ms) and .NET (63 ms) lead.
- **`primes` (45 ms, ~5×), `loop` (38 ms, ~3.6×)** — mostly raw dispatch overhead; `loop` closed
  304 → 38 ms in the 2026-07-16 match-lowering + call-gate round.

`errors-deep` is a reminder that a compute-loop-only view misleads: .NET tops the arithmetic rows
yet is *worst* at deep error recovery (stack-trace capture per throw, ~675 ms); Clojure is heavier
still (~1.3 s). Elixir (OTP 28) is fastest (~6 ms). Brood is 2nd at 39 ms.

- **`pfib` (213 ms, ~1.9× — 2nd, beating Elixir)** — three wins landed 2026-07-02 (Brood repo devlog). First
  the N was bumped 28 → 31 so the row exercises parallel-native *scaling* not task startup/teardown.
  Then two JIT fixes: (1) the two-stage-tiering inlined-upgrade swap used the **shared** global epoch,
  invalidating every peer green process's arm → a cross-process re-tier cascade onto the slow
  IC-dispatch path; the swap now invalidates only the swapping process's fast-links. (2) The inlined
  native was compiled **per-process**; it's now **shared across processes** (one compile serves every
  worker, like the BEAM). Finally the **unboxed-`i64` calling convention** (see `fib` above) removed
  the recursive-call boxing: `pfib` went **847 → 168 ms**, from 5th to **2nd (1.5× off .NET)**, ahead
  of Elixir (286 ms) and Node (299 ms). Parallel scaling itself is already ~93% of the machine's
  OS-process ceiling (Brood green 3.93× vs 4.20× for independent OS processes on this 12-core box —
  it even beats Elixir's 3.30×), so the residual is just `fib`'s single-thread gap (now ~1.5×).

## Wider-range findings (2026-07-12)

Nine benchmarks widened coverage past the numeric/allocation core; they surfaced several concrete
targets, ranked here by value. None are in the positioning-chart aggregate (that stays the original
core-compute rows) — they are reported on their own precisely because they are library/representation
gaps, not core VM speed.

1. **~~Message-passing latency — `pingpong` ~14× behind the BEAM~~ — LARGELY CLOSED (brood, 2026-07-12).**
   Was ~6.6 µs/round-trip (~13× Elixir); now **~2.6 µs (263 ms / 100 k), 3/7 across langs** (ring 4/7) —
   off last place, ahead of Ruby/Node/Python/Clojure. Two fixes: (a) **wake-syscall elision** —
   `enqueue` fired an unconditional `futex_wake` even handing a process to the *current* worker
   (the direct-handoff case); skipping it dropped green↔green ping-pong from ~4.4 futex/round-trip to
   ~0 (202k → ~400 over 100k). (b) **ADR-135: the top-level program now runs as one green process**
   instead of a privileged root thread that blocked on its mailbox condvar and crossed the main↔worker
   boundary via futex *per message*. Both together: pingpong 6.5 → 3.3 µs/RT, futex 416k → 370; ring
   ~2.1 s. Residual ~5.3× vs BEAM is intrinsic to Brood's design (immutable per-message allocation,
   heap-captured migratable continuations, per-process heap-isolated message copies) — not traded away.
   Follow-on: `nest run FILE` now routes through the same program-process path (`%run-program-file`).
   **Follow-on 2 — shared closure arms (brood `d5d670c`, 2026-07-13): ring 2.07 → 1.46 s (~30 %),
   pingpong 341 → 289 ms.** Profiling put ~13 % of `ring` in per-`receive` matcher-closure churn (the
   `receive` macro expands to `((%receive (fn (msg) …) …))`, so every message builds a fresh closure,
   and each build deep-copied the arm `Vec` out of the template cache). `Closure.arms` is now
   `Arc<[ClosureArm]>`, so building from the cache is a refcount bump — killing both the copy and the
   alloc/GC traffic it fed. Sound under the moving GC because a *shared* arms comes only from the
   RUNTIME-keyed template cache (holds only RUNTIME handles a minor collection never relocates), so the
   minor-flush path skips it via `Arc::get_mut`; only the rare def-churn compaction uses `make_mut`.
   Rankings hold (pingpong 3/7, ring 4/7); on the 2026-07-17 run pingpong sits at 263 ms and ring at
   1.4 s, with ring's gap to 3rd (.NET, 885 ms) at ~1.6×.
2. **~~`std/json` super-linear + `std/encoding` (base64) blows RSS~~ — FIXED (brood `a1d3fd2`, 2026-07-12).**
   Both traced to one root cause: **`string->list` was O(n²)** — it built each char with
   `(substring s i (inc i))`, and `substring` walks to char boundary `i` every call, so the
   `(into [] (string->list s))` code-point vector the parsers index was O(n²) *to construct*. Reimplemented
   over the native `string-split` (one O(n) `chars()` pass): `json` went super-linear → linear (2 000 recs
   **2.5 s → 0.9 s**) and `base64` dropped **1.5 s / 1.3 GB RSS → 134 ms / 105 MB** (overtaking Clojure,
   7/7 → 6/7). A companion `seq` fix realises a `bytes` value to a list once (`bytes->list`), killing an
   O(n²) `(reduce … bytes)`; the same char-scan / `(str acc …)` anti-patterns were then swept out of
   `std/csv` / `std/url` / `std/net`. `regex` remains linear-but-interpreted (pure-Brood backtracking that
   re-parses the pattern each `matches?`) — the next-cheapest structural cost on this axis.
3. **Immutable numeric loops — `nbody`, was ~850×, now 66× (317 ms).** Vector work + float-JIT fixes
   (inline `fsqrt`, deopt repair, cached-pointer reads for spilled vectors) took it 5.9 s → 317 ms.
   Rebuilding immutable body vectors every step still dominates the residual; closing further needs
   escape analysis that stack-allocates/reuses the per-step vectors or a native float-array
   primitive (philosophically fraught — see the mutable-data invariant). The remaining gap is a
   known immutable-cost data point more than a target.
4. **~~Non-tail deep recursion — `ackermann` ~16×~~ — FIXED (brood `f90910c`, 2026-07-13): 4.02 → 0.36 s,
   7/7 → 3/7.** The lever wasn't "double-recursion" — profiling showed `ack` was *already* JIT'd, on the
   **boxed** path, not the unboxed-i64 register worker that carries `fib`. Two real blockers: (1) the i64
   worker's subset checker + lowering only recognized a **non-tail** self-call (`Node::Call`, `fib`'s
   argument-position recursion); `ack`'s recursion is in **tail** position (`Node::SelfCall`), which the
   subset never matched, so it fell through. (2) The worker's native-recursion depth cap was a **stale
   1400** — sized for the removed (ADR-100) coroutine stacks — below `ack`'s ~4093 depth, so it
   depth-bailed to boxed regardless. Fix: teach the subset about tail self-calls (recurse into a
   `SelfCall`'s args to find the genuinely-recursive nested `Call`, but keep pure-tail loops on their
   faster self-tail-loop path) + raise the cap to 32768 (stack-safe on the real 16 MiB worker stack).
   Now **3rd**, past Node/Clojure/Ruby/Python. Broad: any mixed tail+non-tail int recursion rides
   registers. The full suite (777 + 4-engine differential fuzzer) stays green; a runaway still raises a
   clean error (depth-bail → boxed drain), not a SIGSEGV.
5. **~~`sieve` ~316× and `persistent-map` ~30×~~ — LARGELY CLOSED (2026-07-16 dense-Table round).**
   The lock-free dense int-key `Table` + JIT-lowered `table-*` ops (with table-base hoisting) took
   `sieve` to **33 ms (~20× .NET, 3rd — ahead of Elixir)** and, with the fused `map-int-add` idiom,
   `persistent-map` to **75 ms (~3.6×, 4th)**. What's left is the expected floor of a Table standing
   in for a mutable bool array and CHAMP path-copy under read-modify-write.

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
3. **`matmul`** (~27× ratio, but .NET is only ~5 ms so it's noise-sensitive; 135 ms absolute is not
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
