# What to expect from Brood — benchmark results

Fifteen small programs, each written **five times** — in Brood, Elixir, Python,
Node, and Ruby — and run under one identical harness. The goal isn't to crown a
winner; it's to give an honest, realistic picture of what you get with Brood and
where it costs you, measured against four well-known runtimes.

> Every program prints a checksum, and the harness verifies **all five languages
> produce the same answer** on every benchmark — so this is the same work, five
> ways, not different amounts of it.

> **Engine:** Brood runs on its bytecode VM (the closure-compiling engine that
> replaced the original tree-walker), with **primitive inlining** — the core
> arithmetic/comparison ops (`+ - * < <= =`) execute inline as native `i64`
> operations instead of through a dispatched call. Three runtime changes show up
> below: a **reducible lazy range** so `(range n)` folds without materialising a
> list (`reduce` 1.58 s → 0.27 s, 130 MB → 20 MB); a **process-count-aware GC
> floor** that cut parallel fan-out's peak memory ~35× (`pfib` ~980 MB → ~28 MB);
> and **routing spawned processes through the VM** (they were tree-walked even
> under the VM), cutting `pfib`'s *wall time* ~4× (3.84 s → ~1 s). The numbers
> below are that engine.

## The honest summary

- **Memory — Brood's clear strength.** A ~11 MB base, holding 11–38 MB across
  *every* workload (the old 130 MB `reduce` outlier is gone — see the engine
  note), versus Elixir's 90–115 MB and Node's 44–69 MB. Startup is ~27 ms: not
  the fastest (Python edges it, Node ties it) but ~12× ahead of Elixir's BEAM, so
  Brood still finishes short tasks before the BEAM has booted.
- **Raw single-threaded compute — Brood's weakest area.** Its bytecode VM is
  young, and on tight loops it trails not just Node's JIT (**~18–30×**) but mature
  bytecode interpreters too: roughly **5–16× slower than Ruby** and **3–7× behind
  Python on tight loops** (more on allocation-heavy work) — both interpreted, no
  JIT, so this isn't a JIT gap, it's headroom left in the VM. Primitive inlining
  narrowed it from the old tree-walker, but compute is where Brood pays.
- **Concurrency depends entirely on the workload.** Cheap, plentiful lightweight
  processes and **concurrent I/O** are a genuine strength: `spawn` now **edges
  out Elixir** (334 ms vs 367 ms, and a third of its memory), and `http` lands
  ~25% behind Node, ahead of Python and Ruby. **Parallel CPU crunching** is
  respectable too: two runtime fixes (below) took `pfib` from 30× off the pack
  and ~980 MB to **~1 s and among the lightest in the field (28 MB)** — still
  last on wall time, but by ~2–5×, not orders of magnitude. Both results are
  below.

---

## Full results — total wall time

The whole process, start to finish (startup + work). 🥇 marks the fastest in
each row. `N` is the workload size.

| benchmark | what it stresses | N | brood | elixir | python | node | ruby |
|-----------|------------------|--:|------:|-------:|-------:|-----:|-----:|
| startup | cold start + base memory | — | 27 ms | 325 ms | **12 ms** 🥇 | 24 ms | 49 ms |
| fib | deep recursion | 30 | 502 ms | 375 ms | 73 ms | **29 ms** 🥇 | 106 ms |
| loop | 3 M-iteration count | 3 M | 545 ms | 363 ms | 191 ms | **30 ms** 🥇 | 110 ms |
| reduce | fold over 1 M numbers | 1 M | 269 ms | 330 ms | **22 ms** 🥇 | 24 ms | 44 ms |
| primes | trial-division | 20 k | 98 ms | 386 ms | **22 ms** 🥇 | 25 ms | 58 ms |
| collatz | tight integer loop | 30 k | 876 ms | 390 ms | 239 ms | **31 ms** 🥇 | 135 ms |
| mandelbrot | floating-point | 128 | 394 ms | 365 ms | 78 ms | **34 ms** 🥇 | 70 ms |
| matmul | nested loops + indexing | 80 | 886 ms | 343 ms | 64 ms | **32 ms** 🥇 | 95 ms |
| strings | string building | 50 k | 348 ms | 631 ms | **28 ms** 🥇 | 39 ms | 83 ms |
| wordcount | hash-map build | 100 k | 864 ms | 333 ms | 34 ms | **29 ms** 🥇 | 55 ms |
| bintree | allocation / GC | 40 | 580 ms | 364 ms | 30 ms | **29 ms** 🥇 | 61 ms |
| sort | sort + checksum walk | 50 k | 140 ms | 329 ms | **36 ms** 🥇 | 37 ms | 53 ms |
| spawn | 20 k lightweight processes | 20 k | **334 ms** 🥇 | 367 ms | — | — | — |
| pfib | 100 fibs **in parallel** | 28 | 1.03 s | 569 ms | 377 ms | **197 ms** 🥇 | 279 ms |
| http | 500 **concurrent** HTTP GETs | 500 | 242 ms | 643 ms | 306 ms | **191 ms** 🥇 | 431 ms |

Three runtime changes show in these numbers. **`reduce` 1.58 s → 0.27 s and
130 MB → 20 MB**: `range` became a **reducible lazy range** — `(range n)` no
longer materialises a million-element list; `reduce`/`fold`/`sum`/`count` iterate
it in a counted loop with zero allocation. That single change took the suite's
former worst result (90× off Python and the one memory outlier) down to ~12× and
roughly Python's memory. **`pfib` 3.84 s → ~1 s**: a spawned process's body was
running on the *tree-walker* even under `BROOD_VM=1`, so every green process was
~4–5× slower than the same code at top level; routing them through the VM closed
that. And **`pfib` peak ~980 MB → ~28 MB**: a process-count-aware GC floor (see
that section). Single-threaded compute is otherwise unchanged — that's the VM's
standing speed, and where Brood still trails the others. (`pfib` is the most
load-sensitive row in the suite; it has bounced between ~0.8 s and ~1.1 s.)

## Biggest gaps — where to focus next

Ranked by how far Brood trails the **fastest other** language (wall) and the
**lightest other** (memory). Worst first — these are the optimization targets;
everything not listed is already within ~2× on at least one axis.

| benchmark | wall gap | mem gap | what it points at |
|-----------|---------:|--------:|-------------------|
| `wordcount` | **30×** | 3.0× | immutable hash-map **insert churn** — the persistent-map (HAMT) build/copy cost. |
| `collatz` | 28× | 2.0× | tight integer loop — raw per-iteration VM dispatch overhead. |
| `matmul` | 28× | 2.0× | nested loops + `vector` indexing — the index path and loop trampoline. |
| `bintree` | 20× | 1.5× | allocation / GC pressure — building and walking many small trees. |
| `loop` / `fib` | ~18× | 1.2× | per-iteration VM dispatch overhead. |
| `strings` / `reduce` | ~12× | 2.2–2.8× | string-building churn / the fold's per-element apply (no longer a memory outlier). |

The through-line now is **single-thread compute** and **immutable-collection
churn** — no outlier left. `reduce` used to stand alone (90× and 130 MB); the
reducible range closed it, so the field is even: general VM loop/dispatch
throughput (`collatz`, `matmul`, `loop`, `fib`) and persistent-structure build
cost (`wordcount`, `bintree`, `strings`). The concurrency and startup rows are
already ahead or close (`spawn` **0.9× — Brood wins**, `http` 1.3×, `startup`
2.3×, `pfib` 5×) — not where the distance is.

---

## Memory & startup — where Brood is light

| | cold start | memory at rest |
|---|---:|---:|
| Python | **12 ms** 🥇 | 9 MB |
| Brood | 27 ms | **11 MB** |
| Node | 24 ms | 45 MB |
| Ruby | 49 ms | 23 MB |
| Elixir | 330 ms | 90 MB |

Memory is the durable win: Brood holds **11–38 MB across every workload** — a
fraction of Elixir's 90–115 MB, well under Node's 44–69 MB, and lighter than
Ruby's steady ~23 MB — staying essentially tied with Python for lightest at rest.
Startup is ~27 ms: Python edges it, Node ties it, Ruby trails at ~49 ms, but it's
still ~12× ahead of Elixir's BEAM, which spends a third of a second warming up.
For short-lived work that's why Brood still beats Elixir end-to-end on the quick
tasks (`primes`, `sort`): the BEAM's compiled code is fast, but Brood has
finished before it's ready.

There used to be one exception — `reduce` at 130 MB, because `(range 1_000_000)`
materialised the whole list where the others stream it. The **reducible lazy
range** (engine note) fixed that: `reduce` now folds the range in a counted loop
with no list at all, at **20 MB** — so there's no longer a single workload where
Brood is the memory outlier.

## Raw compute — Brood's weakest area, and not just versus a JIT

When the work is a tight loop running inside the language, Brood trails everyone.
`matmul` ≈ 0.89 s, `collatz` ≈ 0.88 s, `wordcount` ≈ 0.86 s, `loop` ≈ 0.55 s,
`fib` ≈ 0.50 s — roughly **18–30× slower than Node**, whose JIT compiles to
native code. That much is expected. The more telling comparison is **Ruby** and
**Python**: both are bytecode interpreters with no JIT on by default, and both
still beat Brood — Ruby by **~5–16×** (`fib` 106 ms vs 502 ms, `matmul` 95 ms vs
886 ms), Python by ~3–7× on the tight loops (and more on the allocation-heavy
`bintree`/`wordcount`, where its C-backed mutable structures pull far ahead). So
this isn't a JIT gap; it's headroom left in a young VM. Primitive inlining
narrowed it from the old tree-walker, but the compute engine has real distance to
make up. (Most of **Elixir's** numbers here are just BEAM boot ~330 ms; its
actual compute is fast, and amortizes away in a long-running service.)

If your hot path is number-crunching, Brood is not the tool yet — or push that
work into a Rust-backed builtin (`sort` is Brood's best compute result, 140 ms,
because the sorting itself isn't interpreted; and `reduce` over a `range` now
folds in a Rust counted loop, 0.27 s instead of 1.6 s).

## Parallel CPU work (`pfib`) — fixed from a disaster to merely last

`pfib` computes `fib(28)` **100 times at once**, each language using its
idiomatic parallelism (Brood/Elixir spawn lightweight processes; Node uses
`worker_threads`; Python and Ruby fork a process pool).

| lang | wall | peak RSS |
|---|---:|---:|
| node | **197 ms** 🥇 | 347 MB |
| ruby | 279 ms | **24 MB** 🥇 |
| python | 377 ms | 22 MB |
| elixir | 569 ms | 95 MB |
| brood | 1.03 s | 28 MB |

This row used to be Brood's worst result by far — **3.84 s and ~980 MB**. Two
runtime fixes turned it around:

- **Wall time (3.84 s → ~1 s).** A spawned process's body was running on the
  **tree-walker even under `BROOD_VM=1`** — the `spawn` entry point called the
  tree-walk `apply`, not the VM — so every green process computed ~4–5× slower
  than the identical code at top level. Routing spawned bodies through the VM
  (with its inlined primitives) closed that gap; a single spawned `fib(28)` went
  from 0.66 s to 0.15 s, matching the root thread.
- **Memory (~980 MB → ~28 MB).** Each share-nothing process climbed to its
  single-process GC floor (~64K objects) before its first collection; a
  **process-count-aware GC floor** now divides that budget across the live
  processes, so a wide fan-out collects earlier. Brood is now **far lighter than
  Node (347 MB) and Elixir (95 MB)** here, in the same ~25 MB neighbourhood as
  Python and Ruby.

What's left is honest: Brood is **still last on wall time**, but by ~2–5×, not
30×, and now in the same league as the others — while using a fraction of Node's
and Elixir's memory. The remaining gap is the single-thread VM speed (above), not
the scheduler, which spreads the work across cores fine. (This row saturates
every core, so it's the most load-sensitive in the suite — it has bounced between
~0.8 s and ~1.1 s across runs.)

## Concurrent I/O (`http`) — Brood runs with the front-runners

`http` fires **500 concurrent GETs** at a local server that sleeps 20 ms per
request, so it measures how well each runtime overlaps in-flight requests — pure
I/O concurrency, where raw compute speed barely matters.

| lang | wall | peak RSS |
|---|---:|---:|
| node | **191 ms** 🥇 | 69 MB |
| brood | 242 ms | 84 MB |
| python | 306 ms | 52 MB |
| ruby | 431 ms | **50 MB** 🥇 |
| elixir | 643 ms | 744 MB |

This is the mirror image of `pfib`. Brood's green processes **park** on the
response (its TCP is message-based), so all 500 requests are genuinely in flight
at once — and it lands in the **front group, ~25% behind Node** (242 ms vs
191 ms) and ahead of Python's thread pool. The one cost is memory: with
`net/http` now coming from the brood-net package, peak RSS rose to ~84 MB here —
heavier than Python and Ruby (~50 MB), though still a fraction of Elixir's
744 MB. Ruby's thread-per-request (a fresh `Net::HTTP` connection each) is
slower here, and Elixir's *stdlib* `:httpc` is slow and heavy (real Elixir
services use a third-party client like Finch). When your work is waiting on I/O,
Brood's concurrency model pays off. (This row is latency-sensitive and the
numbers bounce a bit run-to-run; the ordering is stable.)

## Lightweight processes (`spawn`)

Fanning out 20,000 processes that each send one message: Brood now **edges out
Elixir end-to-end** (334 ms vs 367 ms) *and* does it in **38 MB vs Elixir's
111 MB**. Cheap, plentiful processes are a real part of the runtime — note how
different this is from `pfib`: 20,000 *tiny* processes are cheap; 100
*compute-heavy* ones are not.

---

## So when should I use Brood?

**A good fit:**

- Command-line tools and short-lived scripts — fast start, tiny footprint.
- Memory-constrained environments — a fraction of the BEAM's or Node's RAM.
- I/O-bound concurrency — many simultaneous requests/connections, where it's
  competitive with Node and far lighter than stdlib Elixir.

**A poor fit:**

- CPU-bound number crunching — the VM trails not just JITs but Ruby and Python
  too (~5–16× / ~3–7×). Parallel fan-out is no longer a disaster (~1 s, not ~4 s,
  and light on memory), but per-task compute is still the bottleneck — lean on
  Brood for *I/O* concurrency, not *compute* fan-out.
- Immutable-collection churn at scale — building large persistent maps
  (`wordcount`) or many small trees (`bintree`) is where the remaining distance
  is. (Folding a `range`, once the suite's worst case, is now fixed — it streams.)

**Versus Elixir specifically:** they optimize for different moments. Brood wins
the sprint (startup, memory, short tasks, I/O concurrency on a budget); the BEAM
wins the marathon (long-running services where boot cost amortizes and warm
compute and battle-tested libraries matter).

---

## The fine print

- **How it's measured, and why it's fair** → see the [README](README.md)
  (methodology, identical algorithms, how to run it).
- **Raw data** → [`results/report.md`](results/report.md) and
  [`results/results.json`](results/results.json).

_Measured on: Intel Raptor Lake-S (28 cores) · 61 GB RAM · Ubuntu 26.04 · Brood
0.1.0 (bytecode VM + primitive inlining + reducible lazy range +
process-count-aware GC floor + VM-routed spawned processes) · Elixir 1.20.0 /
OTP 29 · Python 3.14.4 · Node
24.15.0 · Ruby 3.3.8. Compute rows are best-of-3 from the full suite; the
latency-sensitive `startup` and `http` rows are best-of-5 measured in isolation
so neighbouring benchmarks' load doesn't inflate them. `pfib` saturates every
core and remains the most load-sensitive row in the suite._
