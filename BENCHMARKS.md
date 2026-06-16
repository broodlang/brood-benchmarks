# Brood Benchmarks

Machine: `whklat`, 12-core x86-64, Linux 7.0.0, 2026-06-16.
Runtimes: Brood 0.1.0 · Elixir 1.20.0 / OTP 28 · Python 3.14.4 · Node 22.21.0 · Ruby 3.3.8 · .NET 10.0.109.
Method: best of 3 runs per benchmark; the concurrency benchmarks (spawn, pfib, http) take the best of 7. Compute = wall − startup, so boot cost is not charged against compute-heavy benchmarks.

> **Isolation.** Each measured process is pinned with `taskset` (single-threaded
> benchmarks to one dedicated core, the concurrency ones to all 12) and the harness
> idles 0.25 s before each run, so a prior run's teardown doesn't bleed into the
> next measurement. Every benchmark prints one integer and the harness asserts all
> six languages produce the **same** checksum — a mismatch fails the run — so we
> know they did equivalent work.
>
> **JIT wins landed.** Admitting bool literals to the JIT subset (Brood `9dfc00f`)
> tiered `primes`' trial-division loop (**351 → 56 ms, now 3rd of six**) and helped
> `nqueens` (**933 → 523 ms**, its bool `safe?` arms tier); left-folding n-ary
> `+`/`*` into native 2-ary ops tiered `bintree`'s `check` (**1123 → 452 ms**). The
> bool win first shipped a JIT miscompile (a `Value::Bool` truthiness check read the
> full payload word instead of the bool byte, corrupting `nest format`); that's
> fixed and guarded by a tiering regression test. Promoting a top-level `(fn …)`'s
> body into the immovable RUNTIME region (Brood `dfa4f67`) — so an inline lambda no
> longer forces its whole form onto the tree-walker — moved **two** rows at once:
> `pipeline` (**552 → 122 ms**, and **→ 39 ms** once it later moved to the fused
> `eduction` path — lazy seq-views, ADR-111) and `matmul`'s matrix construction (**542 → 241 ms**).
> Then lowering `and`/`or` to the JIT (a comparison result crossing a block boundary
> now zero-extends to the block-param width) tiered `mandelbrot`'s `esc` escape test
> (`(and (<= …) (< …))`) — the **single biggest win: 1326 → 250 ms (~5.3×)**, off the
> bottom of the table. (The promotion also surfaced two latent closure-serialisation
> gaps — `form-pos` over the wire, and a `def`-RHS-in-`let` capture — both since fixed.)
> Most recently, **loop-invariant vector hoisting (LICM)** — resolving an invariant
> vector's element base once at the loop entry and inlining the reads, sound with *no*
> alias analysis because Brood data is immutable — inlined `matmul`'s invariant-row `nth`
> (**~241 → ~212 ms compute**).
>
> **2026-06-16 — the call/dispatch round.** Four wins targeting the per-call and
> per-access overhead the profiles flagged. (1) **Sharing JIT'd native code across a
> runtime's processes** — a spawned worker installs an already-compiled arm's code
> pointer instead of recompiling its own copy (10 000 workers no longer swamp the
> background compiler): **`spawn` 516 → 122 ms (~4.2×), from ~7.7× to ~2.5× of Elixir**,
> the biggest single jump. (2) **Hoisting loop-invariant *scalar* global reads** (the
> LICM above, extended from vectors to scalars) — `loop--acc` reads its bound `n` once
> at entry instead of through the inline cache every iteration: **`loop` 190 → 112 ms,
> now at parity with Elixir (~106 ms)**. (3) A **no-clone fast-link** on the JIT call
> path (drop the per-call `Arc` clone) — **`fib` ~654 → 558 ms**. (4) **Lexical
> addressing of captured variables** — a closure reads captures as flat frame slots,
> not env-chain symbol scans (~21 % on capture-heavy closures; campaign benchmarks flat,
> a foundation for closure-heavy editor code). All four keep Emacs-style hot reload
> (the epoch guard / shared epoch deopts on a `def`), validated by the JIT≡tree-walker
> differential + GC-stress + the full suite.

---

## Boot time

Cold start to first instruction. Lower is better.

| runtime | boot |
|---------|------|
| Python  | 11ms |
| Node    | 21ms |
| .NET    | 22ms |
| Brood   | 28ms |
| Ruby    | 44ms |
| Elixir  | 256ms |

Brood is the fourth-fastest boot, ahead of Ruby and ~9× ahead of the BEAM.

---

## Compute times

Wall time minus boot cost. All times in ms unless noted. Lower is better.

### fib(35) — naive recursion

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 558ms | 127ms | 819ms | 81ms | 669ms | 44ms |

Naive double recursion runs on the native path (call linking + call-site inline
cache). Brood matches Ruby and edges out Python; the JITs (.NET, Node) and the BEAM
are still well ahead on raw call throughput.

### loop 30 M — raw iteration

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 112ms | 106ms | 2610ms | 34ms | 612ms | 12ms |

The self-tail loop is JIT'd: Brood beats every interpreter in the field (Python,
Ruby) and is now **at parity with the BEAM** (112 vs 106 ms) — hoisting the
loop-invariant global bound `n` out of the per-iteration inline-cache read closed
the old ~1.6× gap. Only the bare-metal JITs (Node/V8, .NET) lead.

### reduce 5 M — higher-order fold

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 111ms | 37ms | 118ms | 248ms | 244ms | 12ms |

A real fold (`+` applied per element) in all six. Brood's primitive-reducer fast
path **beats Node and Ruby** here — their per-element callback/block folds cost more
than Brood's — and ties Python; .NET and the BEAM lead.

### primes 150 k — trial division

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 43ms | 63ms | 137ms | 11ms | 129ms | 8ms |

**Was 351 ms (last of six).** Admitting bool literals to the JIT subset (Brood
`9dfc00f`) let the `divides-none?` trial-division loop — whose exit arms return
`true`/`false` — tier to native. Now **3rd of six, ahead of Python and Ruby**, ~6×
faster than before.

### collatz 250 k — tight integer loop

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 536ms | 167ms | 2803ms | 189ms | 929ms | 48ms |

`collatz`'s `steps` is an all-integer self-tail loop that runs native; Brood is in
Node's range and far ahead of Python and Ruby.

### mandelbrot 540×540 — floating point

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 239ms | 301ms | 1542ms | 23ms | 458ms | 20ms |

**Was 1326 ms (Brood's worst row — only Python was slower).** `esc`'s escape test is
`(and (<= (+ xx yy) 4.0) (< i maxi))`, and two JIT gaps kept the whole loop off the
native path: `and`/`or` (a comparison result crossing a block boundary was passed at
the wrong width, bailing the arm) and float operands. Lowering `and`/`or` (Brood
`30156ad`) — the float comparisons already had codegen — tiered `esc`: **1326 → 250 ms
(~5.3×)**, the suite's single biggest win. It now beats Elixir and Ruby; only the JITs
lead. (Float *arithmetic* in non-comparison shapes is still the frontier; `mandelbrot`
happens to be all comparisons + adds/muls the JIT already covers.)

### matmul 175×175 — nested loops + array indexing

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 176ms | 83ms | 502ms | 24ms | 324ms | 3ms |

**Was 542 ms; beats Ruby and Python.** The matrix *construction* — `(into [] (map (fn (i)
… (map (fn (j) …))) …))`, two top-level inline lambdas — used to run tree-walked.
Promoting a top-level `(fn …)`'s body into the immovable RUNTIME region (Brood `dfa4f67`)
lets it VM-compile: **~2.2× faster**. The inner `dot` loop already runs native (the old
"data-dependent deopt" note was wrong); its cost was the **per-element `nth`**, a
`brood_rt_vector_ref` call (marshal + a `boxcar` slab lookup + a 24-byte out-pointer copy,
~7–10 ns each). **Loop-invariant vector hoisting (LICM)** resolves an *invariant* vector's
element base once at the loop entry and inlines `ptr + idx*stride` reads — sound with **no
alias analysis** because Brood data is immutable (ADR-026). It inlines both `(nth rowa k)`
(invariant local) and `(nth b k)` (the global `b`, hoisted with a back-edge `global_epoch`
guard that deopts on a concurrent rebind, so it stays bit-identical to the VM's late
binding): **~241 → ~171 ms compute**. The residual gap is the one read it can't hoist — the
per-`k` row — plus the boxed 24-byte `Value` vs .NET's register `long`. .NET does this in
~6 ms, so the ratio (**~30×**, noise-sensitive on that tiny denominator) is still the
suite's largest, but Brood now sits comfortably ahead of both interpreters.

### strings 500 k — comma-join 0..n-1 + length

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 12ms | 130ms | 46ms | 65ms | 96ms | 33ms |

**Was 807 ms (last by far, 181 MB — the memory outlier); now 10 ms, fastest and
lightest of six.** The old code did `(join "," (map number->string (range n)))` — a
redundant `map` that allocated N throwaway strings + a live N-element cons list the GC
then relocated, all of which `%string-join` re-rendered anyway. `join` already renders
each element, so we join the range directly (`(join "," (range n))`), matching Elixir's
`Enum.join(0..(n-1), ",")`. The native `%string-join` now has a **streaming int-range
fast path** — iterate `lo..hi`, format each integer straight into one pre-grown buffer
with `write!` (no intermediate `Vec`, no per-element `String`). Fully immutable — no
string builder; this only changes how the result string is *constructed*.

### wordcount 750 k — hash-map build

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 954ms | 191ms | 190ms | 35ms | 77ms | 39ms |

**This is NOT an immutability cost.** Elixir's `Enum.reduce(… Map.update(m, k, 1, &(&1+1)))`
is the *same* immutable-map read-modify-write into a plain `%{}` — and it's ~5.6× faster
than Brood. So the gap is Brood's young CHAMP's **constant factors**, not the persistent
approach. ~94% of Brood's time is the trie RMW (the LCG arithmetic alone is 70 ms). Two
immutable levers: a single-pass **`map-update`** primitive (Brood does `(assoc m k (+ (get m
k 0) 1))` = *two* trie walks; Elixir's `Map.update` is one), and cheaper CHAMP path-copy
(per-level `SmallVec` clones + a fresh `MapNode` per level). Open.

### wordcount 750 k — hash-map build

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 954ms | 191ms | 190ms | 35ms | 77ms | 39ms |

Immutable CHAMP-map build (Brood/Elixir) vs mutable dict/hash (the rest). The
immutable side pays for structural sharing; Brood also has no map-build JIT path.

### bintree depth 12 ×200 — allocation + GC

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 451ms | 56ms | 105ms | 26ms | 104ms | 14ms |

**Was 1123 ms.** `check` does `(+ 1 (check …) (check …))` — a 3-arg add that used to
route through the variadic prelude `+` and kept the arm off the native path.
Left-folding n-ary `+`/`*` into native 2-ary ops (Brood `dcb4232`) lets it tier:
**~2.5× faster.** Memory stays low (24.8 MB) despite the allocation churn.

### sort 375 k — sort + walk

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 320ms | 129ms | 233ms | 117ms | 76ms | 70ms |

The native sort plus an in-language checksum walk: Brood's **closest compute gap**
in the suite (~4× the fastest).

### nqueens 10 — backtracking recursion

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 610ms | 52ms | 59ms | 11ms | 137ms | 20ms |

**Was 933 ms.** Backtracking whose `safe?` predicate returns `true`/`false` — the
same bool-subset fix that moved `primes` tiers those arms too (**~1.8× faster**).
The remaining cost is the per-step list building the JIT doesn't cover.

### errors 200 k — raise + recover a value (compute ms)

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 210ms | 88ms | 51ms | 636ms | 123ms | 318ms |

Raw exception throughput — raise a value-carrying error and recover it, in a tight loop.
Python's exception machinery is fastest; Brood is 4th (ahead of .NET and Node). A shallow
throw is cheap even in .NET (its cost is the stack-trace capture, which a 1–2-frame throw
barely pays), so this axis alone doesn't separate the runtimes the way real error flows
do — hence `errors-deep`.

### errors-deep 50 k — throw 50 frames deep, catch at the top (compute ms)

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 277ms | 79ms | 238ms | 234ms | 127ms | 770ms |

The realistic shape: an error raised deep in a call stack and recovered near the top (a
driver failing N layers down). **.NET is last (~10× the fastest)** — it captures a full
stack trace on every throw, so the cost scales with depth, exactly where exceptions hurt in
production. Elixir/Ruby lead (the BEAM unwinds cheaply); **Brood is 5th, but still ahead of
.NET.** Both error benchmarks do equivalent work in all six languages (same checksum). This
is where a compute-loop-only suite misleads: **.NET tops the arithmetic rows but is the
*worst* at deep error recovery** — the axis that matters under real-world fault load.

### pipeline 100 k — filter → map → reduce

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 42ms | 14ms | 4ms | 12ms | 8ms | 7ms |

**Was 552 ms (last by a wide margin), then 122 ms, now 39 ms.** A composed `filter → map →
reduce` over a range. Two levers landed. First, promoting the top-level inline `(fn …)`
stages into the immovable RUNTIME region (Brood `dfa4f67`) let the form VM-compile and tier
(**~4.5×**). Then **lazy seq-views** (ADR-111, compute-frontier lever 3c): `eduction` builds a
non-materialising view carrying a transducer, so the chain **fuses into one pass with no
intermediate lists**. That matches the lazy/streaming forms the peers use here (Elixir
`Stream`, Python generators, .NET LINQ — Node and Ruby build eager arrays), and closed the gap
from **~31× to ~8× off the fastest** while dropping peak memory **34 → 13 MB** (~3.5× faster,
~2.6× lighter at this N; ~3.3× / ~13× at n=1e6, where the eager cons-per-stage dominates).
Eager `map`/`filter` stay eager — Brood iterates them for side effects — so fusion is opt-in
via `eduction`/`lmap`/`lfilter`. Still 6/6 here (the per-element transducer closures are
interpreted), but no longer the memory or allocation outlier it was. (`strings`, the other
join-heavy row, is now *first* — see below — by streaming the range straight into the
buffer; no string builder needed.)

### spawn 10 k — concurrent fan-out, each fib(15)

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 122ms | 48ms | 601ms | 57ms | 1732ms | 18ms |

Brood uses green processes + message passing — now **~2.5× of Elixir** (was ~7.7×),
ahead of Node and well ahead of Python's asyncio and Ruby's OS threads. The big jump
(516 → 122 ms): each worker computes `fib(15)`, and workers now **share the JIT'd
native code** for `fib` (one compile across the whole runtime) instead of each
recompiling its own copy and swamping the background compiler — so the fib work runs
native, not interpreted. Spawn/teardown of 10 k processes is now the remaining cost.

### pfib 100 × fib(28) in parallel — CPU parallelism

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 399ms | 117ms | 775ms | 131ms | 484ms | 36ms |

100 × `fib(28)` across cores. Brood finishes **ahead of Ruby and Python** and holds
the **lightest memory in the field** (16.0 MB) while saturating 12 cores; .NET, the
BEAM and Node lead.

### http 500 concurrent GETs — I/O concurrency

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 155ms | 758ms | 193ms | 133ms | 226ms | 162ms |

Brood is **2nd of six** on concurrent I/O — behind only Node, ahead of .NET,
Python, Ruby, and the BEAM. Green processes handle 500 in-flight GETs cleanly.

---

## The short version

- **Memory** is Brood's standout: ~14 MB base, holding the lightest or
  second-lightest peak RSS across nearly every workload (only Python is as light),
  and the single lightest in `pfib` (16.0 MB) while running flat-out on 12 cores.
- **Startup** ~28 ms — fourth, behind Python/Node/.NET, ahead of Ruby, ~9× ahead
  of the BEAM.
- **Concurrency** is competitive: `http` 2nd of six, `pfib` ahead of Ruby and
  Python.
- **Error handling** is a real-world axis the compute loops hide: on deep-stack
  propagation (`errors-deep`) **.NET is last (~10×)** — a full stack-trace capture per
  throw — while Brood is mid-pack, ahead of .NET. So .NET tops the arithmetic rows yet is
  the *worst* at recovering errors raised deep in a call stack (the production-relevant
  shape). See the `errors` / `errors-deep` rows above.
- **Higher-order/iteration**: a real `reduce` fold beats Node and Ruby; JIT'd
  integer loops (`loop`, `collatz`, and now `primes`) beat both interpreters; the
  fusing lazy pipelines (`eduction`/`lmap`, ADR-111) fold `pipeline` in one pass with no
  intermediate lists (**~31× → ~8× off the fastest, 34 → 13 MB**), matching the lazy forms
  Elixir/Python/.NET use; top-level-lambda promotion sped `matmul`'s matrix build
  (**~2.2×**); lowering `and`/`or` tiered
  `mandelbrot`'s escape test — its **biggest win, ~5.3×** — so `mandelbrot` now beats
  Elixir and Ruby instead of trailing the field; and loop-invariant vector hoisting
  (LICM, sound with no alias analysis because the data is immutable) inlined both of
  `matmul`'s invariant `nth`s — the local row and the global `b` (epoch-guarded) —
  (**~241 → ~171 ms**), so `matmul` now beats both interpreters.
- **The weak frontier is raw single-threaded compute on un-JIT'd shapes** — array
  math (`matmul`, still the largest ratio at ~30× — .NET does it in ~6 ms; the LICM
  inlined the invariant reads but the per-`k` row `nth` still calls the slab helper and
  the boxed 24-byte `Value` can't match a register `long`), the immutable map build
  (`wordcount` — not an immutability cost; Elixir's immutable `Map.update` is ~5.6× faster,
  so it's Brood's young CHAMP constant factors), and short-lived allocation (`bintree`).
  (`strings` was here too; streaming `%string-join` made it the fastest of six.) By
  geometric mean across the single-threaded suite Brood lands at **~9.9× the fastest
  runtime** (down from ~12× before the mimalloc allocator backend + the `strings` streaming
  win, ~16× before `and`/`or` tiered `mandelbrot`, and ~19.5× before the JIT fixes; the exact
  figure swings with the sub-10 ms compute times of the fastest runtimes) — mid-pack, ahead of
  Python, with .NET and Node fastest. Brood is built for long-running apps (editors, web
  servers), so it spends some memory for speed — the mimalloc backend cut allocation-heavy work
  ~15–28% at higher steady-state RSS (boot unchanged ~38 ms). See
  [`results/positioning.svg`](results/positioning.svg).
