# Brood Benchmarks

Machine: `whklat`, 12-core x86-64, Linux 7.0.0, 2026-06-15.
Runtimes: Brood 0.1.0 · Elixir 1.20.0 / OTP 28 · Python 3.14.4 · Node 22.21.0 · Ruby 3.3.8 · .NET 10.0.109.
Method: best of 5 runs per benchmark (startup best of 15); the concurrency benchmarks (spawn, pfib, http) take the best of 7. Compute = wall − startup, so boot cost is not charged against compute-heavy benchmarks.

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
> `pipeline` (**552 → 122 ms**) and `matmul`'s matrix construction (**542 → 241 ms**).
> Then lowering `and`/`or` to the JIT (a comparison result crossing a block boundary
> now zero-extends to the block-param width) tiered `mandelbrot`'s `esc` escape test
> (`(and (<= …) (< …))`) — the **single biggest win: 1326 → 250 ms (~5.3×)**, off the
> bottom of the table. (The promotion also surfaced two latent closure-serialisation
> gaps — `form-pos` over the wire, and a `def`-RHS-in-`let` capture — both since fixed.)
> Most recently, **loop-invariant vector hoisting (LICM)** — resolving an invariant
> vector's element base once at the loop entry and inlining the reads, sound with *no*
> alias analysis because Brood data is immutable — inlined `matmul`'s invariant-row `nth`
> (**~241 → ~212 ms compute**).

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
| 654ms | 128ms | 754ms | 85ms | 628ms | 53ms |

Naive double recursion runs on the native path (call linking + call-site inline
cache). Brood matches Ruby and edges out Python; the JITs (.NET, Node) and the BEAM
are still well ahead on raw call throughput.

### loop 30 M — raw iteration

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 190ms | 93ms | 2315ms | 28ms | 604ms | 13ms |

The self-tail loop is JIT'd: Brood beats every interpreter in the field (Python,
Ruby) and trails only the JITs and the BEAM.

### reduce 5 M — higher-order fold

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 104ms | 51ms | 107ms | 229ms | 240ms | 26ms |

A real fold (`+` applied per element) in all six. Brood's primitive-reducer fast
path **beats Node and Ruby** here — their per-element callback/block folds cost more
than Brood's — and ties Python; .NET and the BEAM lead.

### primes 150 k — trial division

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 56ms | 72ms | 128ms | 12ms | 114ms | 12ms |

**Was 351 ms (last of six).** Admitting bool literals to the JIT subset (Brood
`9dfc00f`) let the `divides-none?` trial-division loop — whose exit arms return
`true`/`false` — tier to native. Now **3rd of six, ahead of Python and Ruby**, ~6×
faster than before.

### collatz 250 k — tight integer loop

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 486ms | 158ms | 2447ms | 186ms | 882ms | 60ms |

`collatz`'s `steps` is an all-integer self-tail loop that runs native; Brood is in
Node's range and far ahead of Python and Ruby.

### mandelbrot 540×540 — floating point

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 250ms | 296ms | 1397ms | 18ms | 438ms | 22ms |

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
| 171ms | 82ms | 465ms | 22ms | 306ms | 6ms |

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

### strings 500 k — join + length

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 807ms | 133ms | 42ms | 54ms | 94ms | 46ms |

`(map number->string (range n))` builds a live N-element cons list (eager `map`),
which the copying GC relocates repeatedly — also the suite's memory outlier
(181 MB). A lazy/streaming `map` would fix both; deferred as a design change.

### wordcount 750 k — hash-map build

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 974ms | 190ms | 186ms | 29ms | 69ms | 51ms |

Immutable CHAMP-map build (Brood/Elixir) vs mutable dict/hash (the rest). The
immutable side pays for structural sharing; Brood also has no map-build JIT path.

### bintree depth 12 ×200 — allocation + GC

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 452ms | 65ms | 110ms | 33ms | 107ms | 16ms |

**Was 1123 ms.** `check` does `(+ 1 (check …) (check …))` — a 3-arg add that used to
route through the variadic prelude `+` and kept the arm off the native path.
Left-folding n-ary `+`/`*` into native 2-ary ops (Brood `dcb4232`) lets it tier:
**~2.5× faster.** Memory stays low (24.8 MB) despite the allocation churn.

### sort 375 k — sort + walk

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 282ms | 132ms | 200ms | 118ms | 84ms | 66ms |

The native sort plus an in-language checksum walk: Brood's **closest compute gap**
in the suite (~4× the fastest).

### nqueens 10 — backtracking recursion

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 523ms | 65ms | 63ms | 21ms | 132ms | 19ms |

**Was 933 ms.** Backtracking whose `safe?` predicate returns `true`/`false` — the
same bool-subset fix that moved `primes` tiers those arms too (**~1.8× faster**).
The remaining cost is the per-step list building the JIT doesn't cover.

### errors 200 k — raise + recover a value (compute ms)

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 208ms | 87ms | 52ms | 590ms | 111ms | 301ms |

Raw exception throughput — raise a value-carrying error and recover it, in a tight loop.
Python's exception machinery is fastest; Brood is 4th (ahead of .NET and Node). A shallow
throw is cheap even in .NET (its cost is the stack-trace capture, which a 1–2-frame throw
barely pays), so this axis alone doesn't separate the runtimes the way real error flows
do — hence `errors-deep`.

### errors-deep 50 k — throw 50 frames deep, catch at the top (compute ms)

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 270ms | 68ms | 226ms | 226ms | 118ms | 708ms |

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
| 122ms | 17ms | 9ms | 8ms | 18ms | 22ms |

**Was 552 ms (last by a wide margin).** A composed sequence pipeline (`->>` over
`filter`/`map`/`reduce`) whose `(fn …)` stages are top-level inline lambdas — the whole
form ran tree-walked. Promoting a top-level `(fn …)`'s body into the immovable RUNTIME
region (Brood `dfa4f67`) lets it VM-compile and tier: **~4.5× faster**. The remaining
gap is the eager combinators — each stage still materialises and re-walks the sequence,
where the interpreters stream or drop to C. Lazy combinators are the next lever.

### spawn 10 k — concurrent fan-out, each fib(15)

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 516ms | 67ms | 555ms | 51ms | 1583ms | 18ms |

Brood uses green processes + message passing (≈ Python's asyncio cost here, well
ahead of Ruby's OS threads). Spawn/teardown of 10 k processes dominates over the
trivial fib(15) work.

### pfib 100 × fib(28) in parallel — CPU parallelism

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 404ms | 122ms | 705ms | 114ms | 444ms | 38ms |

100 × `fib(28)` across cores. Brood finishes **ahead of Ruby and Python** and holds
the **lightest memory in the field** (16.0 MB) while saturating 12 cores; .NET, the
BEAM and Node lead.

### http 500 concurrent GETs — I/O concurrency

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 148ms | 730ms | 179ms | 116ms | 208ms | 152ms |

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
  top-level-lambda promotion pulled `pipeline` off the tree-walker (**~4.5×**) and
  sped `matmul`'s matrix build (**~2.2×**); lowering `and`/`or` tiered
  `mandelbrot`'s escape test — its **biggest win, ~5.3×** — so `mandelbrot` now beats
  Elixir and Ruby instead of trailing the field; and loop-invariant vector hoisting
  (LICM, sound with no alias analysis because the data is immutable) inlined both of
  `matmul`'s invariant `nth`s — the local row and the global `b` (epoch-guarded) —
  (**~241 → ~171 ms**), so `matmul` now beats both interpreters.
- **The weak frontier is raw single-threaded compute on un-JIT'd shapes** — array
  math (`matmul`, still the largest ratio at ~30× — .NET does it in ~6 ms; the LICM
  inlined the invariant reads but the per-`k` row `nth` still calls the slab helper and
  the boxed 24-byte `Value` can't match a register `long`), the immutable map build
  (`wordcount`), short-lived allocation (`bintree`), and string building (`strings`). By
  geometric mean across the single-threaded suite Brood lands at **~12× the fastest
  runtime** (down from ~16× before `and`/`or` tiered `mandelbrot`, and ~19.5× before the
  JIT fixes; the exact figure swings with the sub-10 ms compute times of the fastest
  runtimes) — mid-pack, ahead of Python, with .NET and Node fastest. See
  [`results/positioning.svg`](results/positioning.svg).
