# Optimization frontier — where the gaps are and what would move them

Core-dev notes: the *interpretation* of the [benchmark data](BENCHMARKS.md). This is where
implementation suggestions live — the [README](README.md) stays a plain "where we stand" for
everyone else. (The Brood repo's `docs/compute-frontier.md` holds the deeper working notes and
play-by-play; this file is the current benchmark-suite read.)

None of the gaps below are architectural — they are implementation headroom in a young runtime.
Profiling puts ~60 % of an interpreted benchmark's time in the bytecode dispatch loop (`vm_run_bc`),
so the two broad levers are **interpreter-dispatch cost** and **widening JIT coverage**.
Numbers below are from the 2026-07-26 run unless dated otherwise.

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

Still interpreted (or only partly JIT'd) — the weak rows; ratios are Brood's compute vs the fastest
language on that row:

- **`nbody` (311 ms; ~24× Node, ~52× .NET's 6 ms)** — float physics rebuilding immutable body
  vectors every step. Vector + float-JIT work took it from 5.9 s; the residual is the rebuild
  itself. Closing further needs escape analysis that reuses the per-step vectors, or a native
  float-array primitive (philosophically fraught — see the immutability invariant). A known
  immutable-cost data point more than a target.
- **`bintree` (105 ms, 6th — the BEAM is unusually fast here at ~9 ms)** — inline small-vector
  storage closed it to 90 ms once; it has since drifted in the 95–115 ms band run-to-run,
  trading places with Python/Ruby. **The one open watch-item.** Remaining known headroom: the
  non-tail-call safepoints in `check`/`make` block the in-arm alloc inline.
- **`nqueens` (81 ms, ~12×)** — backtracking recursion; the `reduce`-over-`range` per node and the
  non-tail `solve`/`safe?` recursion dominate.
- **`mandelbrot` (171 ms, ~9×)** — `esc` is JIT'd with register-carried f64 params (verified via
  CLIF); the residual is the boxed 24-byte `Value` tagging in the arithmetic itself plus loop
  overhead. Eliding back-edge slot stores was prototyped → ~0 (absorbed by the store buffer;
  don't re-attempt). Near the current JIT floor.
- **`pipeline` (32 ms, ~8×)** — lazy-seq / transducer composition the JIT doesn't cover;
  allocation churn dominates. The known blocker: `eduction`'s step closures capture, and the
  fast-link bails on captures.
- **`sort` (208 ms, ~3.3×)** — `(sort nums)` is already native `%sort-asc`; the cost is *building*
  the input list. It is also the suite's heaviest row for memory (174 MB, 7/7) for the same reason.
- **`matmul` (130 ms; the ~33× ratio is inflated by .NET's 4 ms denominator)** — the inner loop is
  native; the residual is the one read LICM can't hoist plus boxed `Value` array storage.
- **`primes` (43 ms, ~5×), `loop` (37 ms, ~3×)** — raw dispatch overhead; both already closed
  hard (loop was 304 ms before the 2026-07-16 match-lowering + call-gate round).

**Memory is not a frontier row.** Base RSS is **19 MB** — 2nd-lightest of the seven, level with
Ruby, and the lightest of the compiled-class runtimes. The ~28 MB carried in the docs until
2026-07-26 was the *pre-ADR-138* source boot — accurate before the boot cache existed, and still
what a cache miss costs. ADR-138 halved it on 2026-07-19, but the harness took the min wall and the
max RSS across runs, so the post-rebuild populate kept landing in the memory column alone and the
win stayed invisible for a week. Fixed with a discarded warmup run. Worth remembering as a
methodology lesson: an asymmetric best-of/worst-of aggregation will quietly publish a runtime's
worst case on one axis and its best on another, and it hides improvements as readily as it
manufactures regressions.

Closed rows worth remembering when reading ratios: `wordcount` (~13× → 1.1×, LINMAP + dense-Table),
`errors`/`errors-deep` (2nd–3rd — .NET is *worst* at deep error recovery at ~670 ms, a reminder
that compute-loop-only views mislead), `pfib` (2nd, ~93 % of the machine's parallel-scaling
ceiling, ahead of Elixir).

## Wider-range findings (2026-07-12 additions, updated)

Ranked by what's left, not by history — the war-story details live in the Brood repo devlog:

1. **Message-passing latency (`pingpong` 189 ms, `ring` 703 ms — Elixir leads ~2.7–3.8×).** Still
   the widest honest gap, but the smallest it has been. Closed from ~14× by three earlier rounds
   (wake-syscall elision on direct handoff; ADR-135, the top-level program is a green process, so
   no root-thread futex per message; and shared closure arms as `Arc<[ClosureArm]>`), then by
   **ADR-155 on 2026-07-26: `ring` 1.4 s → ~700 ms (−48%), `pingpong` 247 → ~185 ms (−21%)**, which
   took `ring` past .NET into 3rd.

   That round is worth reading for how it was found. Isolating a *self*-send + `receive` — same
   mailbox, same copies, zero cross-process handoff — priced a receive at **820 ns** against
   310 ns for the `send`, and matched `pingpong`'s per-receive cost almost exactly. So the
   remaining gap was never scheduling; the earlier rounds had already flattened that. It was the
   `receive` macro wrapping every clause body in a `(fn () body…)` thunk: ~235 ns per message to
   build and call (vs ~50 ns for a small-vector protocol), and — because `Inst::MakeClosure` is
   outside the JIT subset — it made the *whole matcher arm* unlowerable, so the hot message path
   ran with no native code at all (`BROOD_NO_JIT=1` changed the number by zero). The fix has
   `%receive` only *select* a clause and emits the bodies at the call site, where they compile
   into the owning function.

   What is left is the per-candidate `vm_apply` in the scan (`BROOD_NO_HOF=1` is 197 → 509 ms, so
   that protocol still does real work) over an irreducible floor of per-message immutable copies
   and heap-captured migratable continuations, which is design and is not traded away. Brood beats
   every thread/queue language soundly; Node's `ring` "win" is cooperative single-thread async.
2. **Text codecs (`json` 139 ms, `regex` 84 ms, `base64` 102 ms — all 6/7, ahead of Clojure).**
   Pure-Brood `std/` libraries vs native codecs, by design. The axis surfaced two real `std/` bugs
   (an O(n²) `string->list`; a base64 RSS blow-up), both fixed; then the regex lazy-DFA,
   precompiled patterns, `string->codepoints`, and a compile-cache split + deopt-storm fix took
   all three off last place. The residual ~10–40× is honest interpreted-library cost; next
   structural lever would be a bytes/codepoint fast path shared by all three.
3. **`sieve` 35 ms (3rd) and `persistent-map` 61 ms (4th)** — largely closed by the lock-free
   dense int-key `Table` + JIT-lowered `table-*` ops (+ the fused `map-int-add` idiom). What's
   left is the expected floor of a Table standing in for a mutable bool array, and CHAMP
   path-copy under read-modify-write.
4. **`ackermann` 342 ms (3rd)** — was 4.1 s dead last; the i64 register worker now recognises
   tail self-calls and the stale depth cap is gone. Any mixed tail+non-tail int recursion rides
   registers.

## Candidate levers (rough priority)

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
