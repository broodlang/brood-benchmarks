# Optimization frontier — where the gaps are and what would move them

Core-dev notes: the *interpretation* of the [benchmark data](BENCHMARKS.md). This is where
implementation suggestions live — the [README](README.md) stays a plain "where we stand" for
everyone else. (The Brood repo's `docs/compute-frontier.md` holds the deeper working notes and
play-by-play; this file is the current benchmark-suite read.)

None of the gaps below are architectural — they are implementation headroom in a young runtime.
Profiling puts ~60 % of an interpreted benchmark's time in the bytecode dispatch loop (`vm_run_bc`),
so the two broad levers are **interpreter-dispatch cost** and **widening JIT coverage**.
Numbers below are from the 2026-07-28 (afternoon) run unless dated otherwise.

## What runs native vs interpreted

The tier-1 JIT covers: integer self-tail loops (`loop`, `collatz`), float-comparison loops
(`mandelbrot`), indexed array reads (`matmul`'s inner `dot`, via loop-invariant hoisting — sound
with no alias analysis because Brood data is immutable), **non-tail and tail-position recursion**
(`fib`, `ackermann`), inline small-vector reads (`bintree`), and the JIT-lowered `table-*` ops
(`sieve`). For int-/float-only recursion an **unboxed-i64/f64 register calling convention**
(2026-07-02) carries args/results in registers with an overflow deopt — the lever that took `fib`
227 → 58 ms and `pfib` 847 → 188 ms. A JIT'd caller links straight to a JIT'd callee through an
epoch-guarded in-IR fast-link; workers share one compiled copy of an arm's native code; a `def`
deopts affected code, so hot reload holds.

**The native-stack guard now costs a call (2026-07-27, brood `f11f4cb`) — the newest recoverable
item on this list.** Deep recursion through JIT'd code could run the *native* stack into its guard
page: an abort, so it killed the OS process rather than the green one, and `try`/`catch` never saw
it. The fix stamps `Heap::jit_stack_limit` from the live remaining stack before entering native
code, checks it in every lowered arm's prologue (three instructions), and — because
`jit_native_depth` under-counts recursion that re-enters Rust through `brood_rt_call_slow` — makes
`jit_dispatch_call`'s headroom probe **unconditional** instead of skipping it below depth 64.
Measured cost, three-binary A/B (`26939e2` / `f11f4cb` / `1a3fc1c`, best-of-7, same build flags):
`fib` wall 70 → 86 ms, `pfib` 183 → 239 ms — ~+30% of compute on the two call-bound rows, and
nothing after `f11f4cb` moves them further.

**Recovered the same day (brood `e87cfc1`; `fib` 88 → 74 ms wall, `pfib` 252 → 202, parity with a
guard-deleted build).** Both of the candidates first suspected here were wrong, and measuring beat
reasoning at every step:

- The prologue check was assumed to be "3 instructions, cheap by construction, the part that cannot
  be dropped". It was in fact where the entire cost lived — but not because any one instruction is
  expensive. The byte check ran *alongside* the old `I64_DEPTH_LIMIT` frame-count cap, `bor`-ing
  two results, so every level of a 30 M-call recursion paid two compares. Deleting the count cap —
  which the byte check subsumes, and which the KI-14 crash had itself proved wrong — recovered all
  of it. Dropping a redundant `limit != 0` test (the compare is unsigned; no address is below zero)
  was worth 5 ms more.
- `stamp_stack_limit`'s per-fast-link `stacker::remaining_stack()` probe, named here as the
  suspicious half, measured **exactly zero** on `fib`: `fib` tiers to the i64 register worker, which
  recurses natively and never takes a fast link. The hoist shipped anyway on a different row's
  number — ~5% on `bintree` (130 → 124 ms), which *is* fast-link-bound.
- The unconditional probe in `jit_dispatch_call` remains unmeasured. It is on the slow call path,
  so it is probably nothing — but that was said about the prologue too.

Still interpreted (or only partly JIT'd) — the weak rows; ratios are Brood's compute vs the fastest
language on that row:

- **`nbody` (323 ms; ~23× Node, ~54× .NET's 6 ms)** — float physics rebuilding immutable body
  vectors every step. Vector + float-JIT work took it from 5.9 s; the residual is the rebuild
  itself. Closing further needs escape analysis that reuses the per-step vectors, or a native
  float-array primitive (philosophically fraught — see the immutability invariant). A known
  immutable-cost data point more than a target. **Ruled out 2026-07-28**, same sweep as `bintree`:
  it copies **798** objects per run (6.2 ms of GC, ~2%), does not bail to the VM (323 ms vs 1112 ms
  interpreted), and is flat across the nursery sweep — a bigger nursery makes it 9% *worse*.
- **`bintree` (103 ms, 6th — the BEAM is unusually fast here at ~12 ms)** — inline small-vector
  storage closed it to 90 ms once; it has since drifted in the 95–115 ms band run-to-run,
  trading places with Python/Ruby. **The one open watch-item.** Remaining known headroom: the
  non-tail-call safepoints in `check`/`make` block the in-arm alloc inline. **Ruled out
  2026-07-28:** it is not GC-bound (only 45k objects copied per run, ~5 ms, ~4% of the row), it
  does not bail to the VM (JIT 124 ms vs 405 ms interpreted), and nursery sizing does nothing —
  flat across an 8K→128K floor sweep, and a 2M floor makes it **19% worse**. The cost is the call
  protocol: ~77 ns per node covering four non-tail calls. That is the X-register/call-convention
  redesign, not a tuning knob.
- **`nqueens` (82 ms, ~12×)** — backtracking recursion; the `reduce`-over-`range` per node and the
  non-tail `solve`/`safe?` recursion dominate.
- **`mandelbrot` (168 ms, ~8×)** — `esc` is JIT'd with register-carried f64 params (verified via
  CLIF); the residual is the boxed 24-byte `Value` tagging in the arithmetic itself plus loop
  overhead. Eliding back-edge slot stores was prototyped → ~0 (absorbed by the store buffer;
  don't re-attempt). Near the current JIT floor.
- **`pipeline` (32 ms, ~8×)** — lazy-seq / transducer composition the JIT doesn't cover;
  allocation churn dominates. The known blocker: `eduction`'s step closures capture, and the
  fast-link bails on captures.
- **`sort` (137 ms, ~2.1×) — CLOSED a rank, 6/7 → 5/7 (2026-07-28).** Was 193 ms. Two runtime
  fixes, neither in `%sort-asc` itself:
  1. **The collector's forwarding tables were `HashMap<u32, u32>`s** (brood `46db4405`). The keys
     are slab indices — dense, bounded by the source slab — so hashing them was pure overhead, and
     it dominated collection. `(gc-stats)` on this row: 4 collections copying 946,464 objects spent
     **95.7 ms of a 158 ms run**, i.e. 101 ns per copied object. Dense `Vec<u32>` tables: same
     collections, same objects, **44.6 ms**.
  2. **The JIT deopted on every non-LOCAL pair read** (brood `c9d3fac8`). `(def data (sort …))` puts
     the list in the shared RUNTIME region, and the inline `first`/`rest` deopted on anything but
     LOCAL — per element, until the arm bailed and the whole walk ran on the interpreter. Measured
     77 ns/element against 1 ns for an identical LOCAL list, and *identical to `BROOD_NO_JIT=1`*.
     Non-LOCAL now calls `car`/`cdr` instead of deopting.
  Do not re-optimise the comparator (already unboxed, brood `1749307`). Still the suite's heaviest
  row for memory (201 MB) — the allocation volume is unchanged, only the cost of surviving a
  collection is. (Earlier editions blamed "building the input list", then `seq_items`/`heap.list`;
  both were measured before the two costs above were visible.)
- **`matmul` (128 ms; the ~32× ratio is inflated by .NET's 4 ms denominator)** — the inner loop is
  native; the residual is the one read LICM can't hoist plus boxed `Value` array storage.
- **`primes` (41 ms, ~5×), `loop` (45 ms, ~4×)** — raw dispatch overhead; both already closed
  hard (loop was 304 ms before the 2026-07-16 match-lowering + call-gate round).

**Memory is not a frontier row.** Base RSS is **20 MB** — 3rd-lightest of the seven, a megabyte
behind Ruby, and the lightest of the compiled-class runtimes. (The ~28 MB carried until 2026-07-26 was the
pre-boot-cache source boot: the harness took min wall but max RSS across runs, so the post-rebuild
cache populate kept landing in the memory column alone. Fixed with a warmup run. Methodology lesson
worth keeping — an asymmetric best-of/worst-of aggregation hides improvements as readily as it
manufactures regressions.)

Closed rows worth remembering when reading ratios: `wordcount` (~13× → 1.1×, LINMAP + dense-Table),
`errors`/`errors-deep` (2nd–3rd — .NET is *worst* at deep error recovery at ~670 ms, a reminder
that compute-loop-only views mislead), `pfib` (2nd, ~93 % of the machine's parallel-scaling
ceiling, ahead of Elixir).

## Wider-range findings (2026-07-12 additions, updated)

Ranked by what's left, not by history — the war-story details live in the Brood repo devlog:

1. **Message-passing latency (`pingpong` 188 ms, `ring` 716 ms — Elixir leads ~2.8–3.5×).** Still
   the widest honest gap, but the smallest it has been — closed from ~14× by four rounds, most
   recently ADR-155 (emit `receive` clause bodies at the call site instead of wrapping each in a
   thunk, which also made the matcher arm JIT-lowerable): `ring` −48%, `pingpong` −21%.

   What is left is the per-candidate `vm_apply` in the mailbox scan (`BROOD_NO_HOF=1` is
   197 → 509 ms, so that protocol still does real work) over an irreducible floor of per-message
   immutable copies and heap-captured migratable continuations — design, not traded away. Brood
   beats every thread/queue language soundly; Node's `ring` "win" is cooperative single-thread
   async.
2. **Text codecs (`json` 148 ms, `regex` 88 ms, `base64` 107 ms — all 6/7, ahead of Clojure).**
   Pure-Brood `std/` libraries vs native codecs, by design. The residual ~10–40× is honest
   interpreted-library cost; next structural lever would be a bytes/codepoint fast path shared by
   all three.
3. **`sieve` 36 ms (3rd) and `persistent-map` 63 ms (4th)** — largely closed by the lock-free
   dense int-key `Table` + JIT-lowered `table-*` ops (+ the fused `map-int-add` idiom). What's
   left is the expected floor of a Table standing in for a mutable bool array, and CHAMP
   path-copy under read-modify-write.
4. **`ackermann` 360 ms (3rd)** — was 4.1 s dead last; the i64 register worker now recognises
   tail self-calls and the stale depth cap is gone. Any mixed tail+non-tail int recursion rides
   registers.

## Candidate levers (rough priority)

0. ~~**Hoist `stamp_stack_limit` out of `jit_run_fast_link`**~~ — **DONE 2026-07-27, and the
   diagnosis in this entry was wrong.** The KI-14 cost is recovered (`fib` 88 → 74 ms, `pfib`
   252 → 202 ms, parity with a guard-deleted build), but not by the hoist: `fib` tiers to the
   **i64 register worker**, recurses natively and never takes a fast link, so hoisting the stamp
   measured *exactly zero* on it. The cost was the per-frame **prologue** guard — specifically
   that the byte check ran alongside the old `I64_DEPTH_LIMIT` frame-count cap, so every level of
   a ~30 M-call recursion paid two compares instead of one. Deleting the count cap (a frame count
   is only ever right for one frame size — which is what KI-14 was) recovered all of it; the
   `0`-limit case it had covered moved to a once-per-outermost-activation check in the i64
   wrapper. The hoist shipped anyway on its own number: ~5% on `bintree` (130 → 124 ms), the
   fast-link-heavy row, and flat everywhere else. Guard intact —
   `tests/jit_deep_recursion_test.blsp` passes at unchanged wall time. (brood `e87cfc1`; full
   attribution table in that repo's `docs/devlog.md`.)
1. **Heap-walking / allocation-heavy code** (`nqueens`, `pipeline`) — the structure-walkers still
   don't tier and some heap reads go through per-op FFI callbacks. The inline small-vector
   storage + read template is proven; extending it to variable-index reads and in-arm alloc
   (blocked by non-tail-call safepoints) is the remaining win toward Elixir. `pipeline`
   additionally wants the capturing-closure fast-link (fill capture slots in the fast frame).
2. **True call inlining / bounded unroll** — removes calls rather than cheapening them; the
   remaining `fib`-class lever. (A measured attempt to move call frame-setup into JIT IR
   regressed and was reverted — the FFI boundary is not the bottleneck.)
3. **Interpreter dispatch** — the ~60 % `vm_run_bc` share bounds every un-JIT'd row.
4. **LINMAP wider coverage** — next target is `reduce`-style folds over non-integer values
   (needs Tables holding non-serialisable `Value`s, or a type-directed variant).
5. **`matmul`/`nbody` unboxed storage** — a boxed 24-byte `Value` vs a register `long`/`double`;
   any unboxed-array design must not violate the immutability invariant.

Dead ends (measured; don't re-attempt): float back-edge store elision (~0 — store buffer),
in-IR call frame-setup (reverted), always-on native-call timing (8–22 % on message rows).

See [`results/report.md`](results/report.md) for the current numbers and
[`results/positioning.svg`](results/positioning.svg) for the compute-vs-memory map.
