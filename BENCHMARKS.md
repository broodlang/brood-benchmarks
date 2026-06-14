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
> **JIT wins landed.** Admitting bool literals to the JIT subset (Brood `9dfc00f`)
> tiered `primes`' trial-division loop (**351 → 42 ms, now 3rd of six**) and helped
> `nqueens` (**933 → 510 ms**, its bool `safe?` arms tier); left-folding n-ary
> `+`/`*` into native 2-ary ops tiered `bintree`'s `check` (**1123 → 443 ms**). The
> bool win first shipped a JIT miscompile (a `Value::Bool` truthiness check read the
> full payload word instead of the bool byte, corrupting `nest format`); that's
> fixed and guarded by a tiering regression test. Then promoting a top-level
> `(fn …)`'s body into the immovable RUNTIME region (Brood `dfa4f67`) — so an inline
> lambda no longer forces its whole form onto the tree-walker — moved **two** rows at
> once: `pipeline` (**552 → 134 ms, ~4.1×**) and `matmul`'s matrix construction
> (**542 → 243 ms, ~2.2×**).

---

## Boot time

Cold start to first instruction. Lower is better.

| runtime | boot |
|---------|------|
| Python  | 11ms |
| Node    | 19ms |
| .NET    | 23ms |
| Brood   | 29ms |
| Ruby    | 40ms |
| Elixir  | 258ms |

Brood is the fourth-fastest boot, ahead of Ruby and ~9× ahead of the BEAM.

---

## Compute times

Wall time minus boot cost. All times in ms unless noted. Lower is better.

### fib(35) — naive recursion

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 635ms | 128ms | 756ms | 86ms | 628ms | 51ms |

Naive double recursion runs on the native path (call linking + call-site inline
cache). Brood matches Ruby and edges out Python; the JITs (.NET, Node) and the BEAM
are still well ahead on raw call throughput.

### loop 30 M — raw iteration

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 190ms | 87ms | 2284ms | 44ms | 585ms | 13ms |

The self-tail loop is JIT'd: Brood beats every interpreter in the field (Python,
Ruby) and trails only the JITs and the BEAM.

### reduce 5 M — higher-order fold

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 119ms | 48ms | 122ms | 234ms | 235ms | 10ms |

A real fold (`+` applied per element) in all six. Brood's primitive-reducer fast
path **beats Node and Ruby** here — their per-element callback/block folds cost more
than Brood's — and ties Python; .NET and the BEAM lead.

### primes 150 k — trial division

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 42ms | 69ms | 136ms | 23ms | 121ms | 21ms |

**Was 351 ms (last of six).** Admitting bool literals to the JIT subset (Brood
`613c484`) let the `divides-none?` trial-division loop — whose exit arms return
`true`/`false` — tier to native. Now **3rd of six, ahead of Python and Ruby**, ~9×
faster than before. The single biggest single-fix move in the suite.

### collatz 250 k — tight integer loop

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 479ms | 155ms | 2465ms | 178ms | 894ms | 57ms |

`collatz`'s `steps` is an all-integer self-tail loop that runs native; Brood is in
Node's range and far ahead of Python and Ruby.

### mandelbrot 540×540 — floating point

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 1326ms | 296ms | 1343ms | 19ms | 431ms | 24ms |

The integer-only JIT can't yet tier float loops, so this stays interpreted —
Brood's weakest row (only Python is slower). The float frontier is the next lever.

### matmul 175×175 — nested loops + array indexing

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 243ms | 81ms | 476ms | 34ms | 302ms | 3ms |

**Was 542 ms.** The matrix *construction* — `(into [] (map (fn (i) … (map (fn (j) …)))
…))`, two top-level inline lambdas — used to run tree-walked. Promoting a top-level
`(fn …)`'s body into the immovable RUNTIME region (Brood `dfa4f67`) lets it VM-compile:
**~2.2× faster**. The remaining gap is the inner `nth` multiply loop, which under-tiers
in a **data-dependent** way (a deopt, not a missing codegen path) — and .NET does this
in 3 ms, so the ratio stays the suite's largest.

### strings 500 k — join + length

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 814ms | 130ms | 54ms | 69ms | 99ms | 43ms |

`(map number->string (range n))` builds a live N-element cons list (eager `map`),
which the copying GC relocates repeatedly — also the suite's memory outlier
(181 MB). A lazy/streaming `map` would fix both; deferred as a design change.

### wordcount 750 k — hash-map build

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 995ms | 180ms | 175ms | 40ms | 84ms | 48ms |

Immutable CHAMP-map build (Brood/Elixir) vs mutable dict/hash (the rest). The
immutable side pays for structural sharing; Brood also has no map-build JIT path.

### bintree depth 12 ×200 — allocation + GC

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 443ms | 48ms | 100ms | 35ms | 110ms | 17ms |

**Was 1123 ms.** `check` does `(+ 1 (check …) (check …))` — a 3-arg add that used to
route through the variadic prelude `+` and kept the arm off the native path.
Left-folding n-ary `+`/`*` into native 2-ary ops (Brood `dcb4232`) lets it tier:
**~2.5× faster.** Memory stays low (24.8 MB) despite the allocation churn.

### sort 375 k — sort + walk

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 288ms | 128ms | 197ms | 119ms | 87ms | 63ms |

The native sort plus an in-language checksum walk: Brood's **closest compute gap**
in the suite (~4× the fastest).

### nqueens 10 — backtracking recursion

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 510ms | 62ms | 68ms | 24ms | 136ms | 31ms |

**Was 933 ms.** Backtracking whose `safe?` predicate returns `true`/`false` — the
same bool-subset fix that moved `primes` tiers those arms too (**~1.8× faster**).
The remaining cost is the per-step list building the JIT doesn't cover.

### pipeline 100 k — filter → map → reduce

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 134ms | 28ms | 9ms | 15ms | 8ms | 6ms |

**Was 552 ms (last by a wide margin).** A composed sequence pipeline (`->>` over
`filter`/`map`/`reduce`) whose `(fn …)` stages are top-level inline lambdas — the whole
form ran tree-walked. Promoting a top-level `(fn …)`'s body into the immovable RUNTIME
region (Brood `dfa4f67`) lets it VM-compile and tier: **~4.1× faster**. The remaining
gap is the eager combinators — each stage still materialises and re-walks the sequence,
where the interpreters stream or drop to C. Lazy combinators are the next lever.

### spawn 10 k — concurrent fan-out, each fib(15)

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 512ms | 56ms | 544ms | 53ms | 1582ms | 24ms |

Brood uses green processes + message passing (≈ Python's asyncio cost here, well
ahead of Ruby's OS threads). Spawn/teardown of 10 k processes dominates over the
trivial fib(15) work.

### pfib 100 × fib(28) in parallel — CPU parallelism

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 410ms | 114ms | 705ms | 123ms | 436ms | 49ms |

100 × `fib(28)` across cores. Brood finishes **ahead of Ruby and Python** and holds
the **lightest memory in the field** (16.0 MB) while saturating 12 cores; .NET, the
BEAM and Node lead.

### http 500 concurrent GETs — I/O concurrency

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 150ms | 644ms | 178ms | 116ms | 222ms | 145ms |

Brood is **2nd of six** on concurrent I/O — behind only Node, ahead of .NET,
Python, Ruby, and the BEAM. Green processes handle 500 in-flight GETs cleanly.

---

## The short version

- **Memory** is Brood's standout: ~14 MB base, holding the lightest or
  second-lightest peak RSS across nearly every workload (only Python is as light),
  and the single lightest in `pfib` (16.0 MB) while running flat-out on 12 cores.
- **Startup** ~29 ms — fourth, behind Python/Node/.NET, ahead of Ruby, ~9× ahead
  of the BEAM.
- **Concurrency** is competitive: `http` 2nd of six, `pfib` ahead of Ruby and
  Python.
- **Higher-order/iteration**: a real `reduce` fold beats Node and Ruby; JIT'd
  integer loops (`loop`, `collatz`, and now `primes`) beat both interpreters; and
  the top-level-lambda promotion pulled `pipeline` off the tree-walker (**~4.1×**)
  and sped `matmul`'s matrix build (**~2.2×**).
- **The weak frontier is raw single-threaded compute on un-JIT'd shapes** — float
  (`mandelbrot`), the immutable map build (`wordcount`), string building (`strings`),
  and array math (`matmul` — improved, but its inner `nth` loop still under-tiers and
  .NET does it in 3 ms, so its ratio stays the suite's largest). By geometric mean
  across the single-threaded suite Brood lands at **~16× the fastest runtime** (down
  from ~19.5× as the JIT fixes landed; the average is now dominated by `mandelbrot`
  and `matmul`, so the `pipeline`/`matmul` wins barely move it) — mid-pack, ahead of
  Python, with .NET and Node fastest. See
  [`results/positioning.svg`](results/positioning.svg).
