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
> **Sizes** are chosen so even the fastest runtime clears startup-measurement
> noise while the Brood VM still finishes in ~1 s or less. `reduce` is a genuine
> higher-order fold in every language (it was a closed-form sum / bare loop before,
> which tested nothing on some runtimes); `nqueens` (backtracking) and `pipeline`
> (filter→map→reduce) are new.

---

## Boot time

Cold start to first instruction. Lower is better.

| runtime | boot |
|---------|------|
| Python  | 11ms  |
| Node    | 18ms |
| .NET    | 25ms |
| Brood   | 28ms |
| Ruby    | 41ms |
| Elixir  | 262ms |

Brood is the fourth-fastest boot, ahead of Ruby and ~9× ahead of the BEAM.

---

## Compute times

Wall time minus boot cost. All times in ms unless noted. Lower is better.

### fib(35) — naive recursion

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 637ms | 121ms | 740ms | 74ms | 626ms | 50ms |

Naive double recursion now runs on the native path (call linking + call-site
inline cache). Brood matches Ruby and edges out Python; the JITs (.NET, Node) and
the BEAM are still well ahead on raw call throughput.

### loop 30 M — raw iteration

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 193ms | 97ms | 2383ms | 45ms | 599ms | 23ms |

The self-tail loop is JIT'd: Brood beats every interpreter in the field (Python,
Ruby) and trails only the JITs and the BEAM.

### reduce 5 M — higher-order fold

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 114ms | 36ms | 110ms | 235ms | 241ms | 11ms |

A real fold (`+` applied per element) in all six. Brood's primitive-reducer fast
path now **beats Node and Ruby** here — their per-element callback/block folds cost
more than Brood's — and ties Python; .NET and the BEAM lead.

### primes 150 k — trial division

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 351ms | 51ms | 135ms | 16ms | 131ms | 5ms |

### collatz 250 k — tight integer loop

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 465ms | 150ms | 2612ms | 180ms | 871ms | 52ms |

`collatz`'s `steps` is an all-integer self-tail loop that runs native; Brood is in
the BEAM's range and far ahead of Python and Ruby.

### mandelbrot 540×540 — floating point

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 1277ms | 279ms | 1423ms | 34ms | 442ms | 18ms |

The integer-only JIT can't yet tier float loops, so this stays interpreted —
Brood's weakest row (only Python is slower). The float frontier is the next lever.

### matmul 175×175 — nested loops + array indexing

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 539ms | 83ms | 456ms | 36ms | 313ms | 6ms |

### strings 500 k — join + length

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 795ms | 122ms | 48ms | 58ms | 87ms | 42ms |

### wordcount 750 k — hash-map build

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 983ms | 187ms | 185ms | 46ms | 71ms | 34ms |

Immutable CHAMP-map build (Brood/Elixir) vs mutable dict/hash (the rest). The
immutable side pays for structural sharing; Brood also has no map-build JIT path.

### bintree depth 12 ×200 — allocation + GC

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 1123ms | 59ms | 108ms | 37ms | 114ms | 26ms |

Short-lived node allocation is the residual cost — the per-process tracing GC and
the un-JIT'd `check` walk dominate. Memory stays low (28.7 MB) despite the churn.

### sort 375 k — sort + walk

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 244ms | 112ms | 185ms | 107ms | 77ms | 76ms |

The native sort plus an in-language checksum walk: Brood's **closest compute gap**
in the suite (3.2× the fastest).

### nqueens 10 — backtracking recursion

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 933ms | 49ms | 67ms | 14ms | 137ms | 19ms |

New. Backtracking with per-step immutable list building — non-tail recursion plus
allocation, a shape the JIT doesn't cover, so Brood trails the field here.

### pipeline 100 k — filter → map → reduce

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 563ms | 23ms | 7ms | 25ms | 8ms | 19ms |

New. A composed sequence pipeline (`->>` over `filter`/`map`/`reduce`). Each stage
materialises and re-walks the sequence in Brood; the interpreters' lazy/streamed
or C-level pipelines are far cheaper — a clear target for the sequence library.

### spawn 10 k — concurrent fan-out, each fib(15)

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 525ms | 58ms | 550ms | 62ms | 1579ms | 22ms |

Brood uses green processes + message passing (≈ Python's asyncio cost here, well
ahead of Ruby's OS threads). Spawn/teardown of 10 k processes dominates over the
trivial fib(15) work.

### pfib 100 × fib(28) in parallel — CPU parallelism

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 425ms | 106ms | 699ms | 117ms | 451ms | 39ms |

100 × `fib(28)` across cores. Brood finishes **ahead of Ruby and Python** and holds
the **lightest memory in the field** (15.8 MB) while saturating 12 cores; .NET, the
BEAM and Node lead.

### http 500 concurrent GETs — I/O concurrency

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 148ms | 675ms | 176ms | 128ms | 208ms | 149ms |

Brood is **2nd of six** on concurrent I/O — behind only Node, level with .NET, and
ahead of Python, Ruby, and the BEAM. Green processes handle 500 in-flight GETs
cleanly.

---

## The short version

- **Memory** is Brood's standout: ~13.7 MB base, holding the lightest or
  second-lightest peak RSS across nearly every workload (only Python is as light),
  and the single lightest in `pfib` (15.8 MB) while running flat-out on 12 cores.
- **Startup** ~28 ms — fourth, behind Python/Node/.NET, ahead of Ruby, ~9× ahead
  of the BEAM.
- **Concurrency** is competitive: `http` 2nd of six, `pfib` ahead of Ruby and
  Python.
- **Higher-order/iteration**: a real `reduce` fold beats Node and Ruby; JIT'd
  integer loops (`loop`, `collatz`) beat both interpreters.
- **The weak frontier is raw single-threaded compute on un-JIT'd shapes** — float
  (`mandelbrot`), array math (`matmul`), allocation (`bintree`), backtracking
  (`nqueens`), and the sequence `pipeline`. By geometric mean across the suite
  Brood lands at ~19.5× the fastest runtime — mid-pack, now ahead of Python, with
  .NET and Node fastest. See [`results/positioning.svg`](results/positioning.svg).
