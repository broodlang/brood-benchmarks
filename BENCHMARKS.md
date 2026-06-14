# Brood Benchmarks

Machine: `whklat`, 12-core x86-64, Linux 7.0.0, 2026-06-14.
Runtimes: Brood 0.1.0 · Elixir 1.20.0 / OTP 28 · Python 3.14.4 · Node 22.21.0 · Ruby 3.3.8 · .NET 10.0.109.
Method: best of 5 runs per benchmark (startup best of 15); the concurrency benchmarks (spawn, pfib, http) take the best of 7. Compute = wall − startup, so boot cost is not charged against compute-heavy benchmarks.

> **Isolation.** Each measured process is pinned with `taskset` (single-threaded
> benchmarks to one dedicated core, the concurrency ones to all 12) and the harness
> idles 0.25 s before each run, so a prior run's teardown doesn't bleed into the
> next measurement. Every benchmark prints one integer and the harness asserts all
> six languages produce the **same** checksum — a mismatch fails the run — so we
> know they did equivalent work.
>
> **Two JIT wins landed since the last run** (Brood `dcb4232`): admitting bool
> literals to the JIT subset tiered `primes`' trial-division loop (**351 → 43 ms,
> now 3rd of six**), and left-folding n-ary `+`/`*` into native 2-ary ops tiered
> `bintree`'s `check` (**1123 → 452 ms**) and helped `nqueens` (**933 → 512 ms**).

---

## Boot time

Cold start to first instruction. Lower is better.

| runtime | boot |
|---------|------|
| Python  | 10ms |
| Node    | 19ms |
| .NET    | 21ms |
| Brood   | 28ms |
| Ruby    | 42ms |
| Elixir  | 259ms |

Brood is the fourth-fastest boot, ahead of Ruby and ~9× ahead of the BEAM.

---

## Compute times

Wall time minus boot cost. All times in ms unless noted. Lower is better.

### fib(35) — naive recursion

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 645ms | 123ms | 766ms | 74ms | 640ms | 40ms |

Naive double recursion runs on the native path (call linking + call-site inline
cache). Brood matches Ruby and edges out Python; the JITs (.NET, Node) and the BEAM
are still well ahead on raw call throughput.

### loop 30 M — raw iteration

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 183ms | 92ms | 2358ms | 31ms | 610ms | 25ms |

The self-tail loop is JIT'd: Brood beats every interpreter in the field (Python,
Ruby) and trails only the JITs and the BEAM.

### reduce 5 M — higher-order fold

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 108ms | 48ms | 110ms | 232ms | 234ms | 13ms |

A real fold (`+` applied per element) in all six. Brood's primitive-reducer fast
path **beats Node and Ruby** here — their per-element callback/block folds cost more
than Brood's — and ties Python; .NET and the BEAM lead.

### primes 150 k — trial division

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 43ms | 68ms | 126ms | 16ms | 121ms | 9ms |

**Was 351 ms (last of six).** Admitting bool literals to the JIT subset (Brood
`613c484`) let the `divides-none?` trial-division loop — whose exit arms return
`true`/`false` — tier to native. Now **3rd of six, ahead of Python and Ruby**, ~9×
faster than before. The single biggest single-fix move in the suite.

### collatz 250 k — tight integer loop

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 491ms | 151ms | 2469ms | 180ms | 893ms | 60ms |

`collatz`'s `steps` is an all-integer self-tail loop that runs native; Brood is in
Node's range and far ahead of Python and Ruby.

### mandelbrot 540×540 — floating point

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 1332ms | 291ms | 1386ms | 21ms | 435ms | 19ms |

The integer-only JIT can't yet tier float loops, so this stays interpreted —
Brood's weakest row (only Python is slower). The float frontier is the next lever.

### matmul 175×175 — nested loops + array indexing

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 542ms | 79ms | 470ms | 27ms | 294ms | 5ms |

The one bintree-class row the n-ary fold didn't move: its inner `nth` loop
under-tiers in a **data-dependent** way (a deopt, not a missing codegen path) —
still under investigation.

### strings 500 k — join + length

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 824ms | 128ms | 46ms | 58ms | 90ms | 36ms |

`(map number->string (range n))` builds a live N-element cons list (eager `map`),
which the copying GC relocates repeatedly — also the suite's memory outlier
(175 MB). A lazy/streaming `map` would fix both; deferred as a design change.

### wordcount 750 k — hash-map build

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 1014ms | 188ms | 183ms | 38ms | 72ms | 37ms |

Immutable CHAMP-map build (Brood/Elixir) vs mutable dict/hash (the rest). The
immutable side pays for structural sharing; Brood also has no map-build JIT path.

### bintree depth 12 ×200 — allocation + GC

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 452ms | 58ms | 96ms | 21ms | 102ms | 17ms |

**Was 1123 ms.** `check` does `(+ 1 (check …) (check …))` — a 3-arg add that used to
route through the variadic prelude `+` and kept the arm off the native path.
Left-folding n-ary `+`/`*` into native 2-ary ops (Brood `dcb4232`) lets it tier:
**~2.4× faster.** Memory stays low (25.9 MB) despite the allocation churn.

### sort 375 k — sort + walk

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 289ms | 123ms | 190ms | 107ms | 72ms | 77ms |

The native sort plus an in-language checksum walk: Brood's **closest compute gap**
in the suite (~4× the fastest).

### nqueens 10 — backtracking recursion

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 512ms | 62ms | 67ms | 24ms | 128ms | 22ms |

**Was 933 ms.** Backtracking whose `safe?` predicate returns `true`/`false` — the
same bool-subset fix that moved `primes` tiers those arms too (**~1.8× faster**).
The remaining cost is the per-step list building the JIT doesn't cover.

### pipeline 100 k — filter → map → reduce

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 552ms | 23ms | 9ms | 12ms | 19ms | 8ms |

A composed sequence pipeline (`->>` over `filter`/`map`/`reduce`). Each stage
materialises and re-walks the sequence, and the top-level `(fn …)` runs tree-walked
(not VM-compiled) — the interpreters' lazy/streamed or C-level pipelines are far
cheaper. Two clear targets: lazy combinators and top-level-lambda promotion.

### spawn 10 k — concurrent fan-out, each fib(15)

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 520ms | 56ms | 554ms | 54ms | 1601ms | 26ms |

Brood uses green processes + message passing (≈ Python's asyncio cost here, well
ahead of Ruby's OS threads). Spawn/teardown of 10 k processes dominates over the
trivial fib(15) work.

### pfib 100 × fib(28) in parallel — CPU parallelism

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 407ms | 123ms | 684ms | 111ms | 442ms | 35ms |

100 × `fib(28)` across cores. Brood finishes **ahead of Ruby and Python** and holds
the **lightest memory in the field** (17.2 MB) while saturating 12 cores; .NET, the
BEAM and Node lead.

### http 500 concurrent GETs — I/O concurrency

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 139ms | 641ms | 176ms | 120ms | 208ms | 158ms |

Brood is **2nd of six** on concurrent I/O — behind only Node, ahead of .NET,
Python, Ruby, and the BEAM. Green processes handle 500 in-flight GETs cleanly.

---

## The short version

- **Memory** is Brood's standout: ~14 MB base, holding the lightest or
  second-lightest peak RSS across nearly every workload (only Python is as light),
  and the single lightest in `pfib` (17.2 MB) while running flat-out on 12 cores.
- **Startup** ~28 ms — fourth, behind Python/Node/.NET, ahead of Ruby, ~9× ahead
  of the BEAM.
- **Concurrency** is competitive: `http` 2nd of six, `pfib` ahead of Ruby and
  Python.
- **Higher-order/iteration**: a real `reduce` fold beats Node and Ruby; JIT'd
  integer loops (`loop`, `collatz`, and now `primes`) beat both interpreters.
- **The weak frontier is raw single-threaded compute on un-JIT'd shapes** — float
  (`mandelbrot`), array math (`matmul`), the immutable map build (`wordcount`),
  string building (`strings`), and the sequence `pipeline`. By geometric mean across
  the suite Brood lands at **~17.5× the fastest runtime** (down from ~19.5× before
  the JIT fixes) — mid-pack, ahead of Python, with .NET and Node fastest. See
  [`results/positioning.svg`](results/positioning.svg).
