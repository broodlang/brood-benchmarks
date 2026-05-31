# What to expect from Brood — benchmark results

Fifteen small programs, each written **four times** — in Brood, Elixir, Python,
and Node — and run under one identical harness. The goal isn't to crown a winner;
it's to give an honest, realistic picture of what you get with Brood and where
it costs you, measured against three well-known runtimes.

> Every program prints a checksum, and the harness verifies **all four languages
> produce the same answer** on every benchmark — so this is the same work, four
> ways, not different amounts of it.

> **Engine:** Brood runs on its bytecode VM (the closure-compiling engine that
> replaced the original tree-walker). This round adds **primitive inlining** —
> the core arithmetic/comparison ops (`+ - * < <= =`) execute inline as native
> `i64` operations instead of going through a dispatched call — plus a faster
> per-call cache lookup. Together they cut the compute-bound times by a further
> **~1.5–2× over the previous VM** (e.g. `fib` and `loop` more than halved). The
> newest change is a **process-count-aware GC floor** that cut parallel
> fan-out's peak memory ~10× (`pfib` ~980 MB → ~100 MB; see that section). The
> numbers below are that engine.

## The honest summary

- **Memory — Brood's clear strength.** A ~11 MB base, holding 11–37 MB across
  most workloads, versus Elixir's 90–115 MB and Node's 44–69 MB. Startup is
  ~24 ms: not the fastest (Python and Node both edge it, within a few ms) but
  ~13× ahead of Elixir's BEAM, so Brood still finishes short tasks before the
  BEAM has booted.
- **Raw single-threaded compute — slower, but much closer than it was.** As a
  bytecode interpreter Brood still trails a JIT, but primitive inlining narrowed
  the gap a lot: tight loops and recursion now run roughly **12–35× slower than
  Node** (down from 25–90×), and 2–15× behind Python.
- **Concurrency depends entirely on the workload.** Cheap, plentiful lightweight
  processes and **concurrent I/O** are a genuine strength (it lands within ~25%
  of Node on the HTTP test, ahead of Python). **Parallel CPU crunching** is still
  slow per task — an interpreter racing a JIT, 100 ways at once — but it's no
  longer memory-hungry: a GC-floor fix (below) cut `pfib`'s peak from ~980 MB to
  ~100 MB, in line with Elixir and a third of Node's. Both results are below.

---

## Full results — total wall time

The whole process, start to finish (startup + work). 🥇 marks the fastest in
each row. `N` is the workload size.

| benchmark | what it stresses | N | brood | elixir | python | node |
|-----------|------------------|--:|------:|-------:|-------:|-----:|
| startup | cold start + base memory | — | 22 ms | 308 ms | **12 ms** 🥇 | 21 ms |
| fib | deep recursion | 30 | 361 ms | 415 ms | 74 ms | **32 ms** 🥇 |
| loop | 3 M-iteration count | 3 M | 426 ms | 398 ms | 185 ms | **26 ms** 🥇 |
| reduce | fold over 1 M numbers | 1 M | 1.45 s | 309 ms | **18 ms** 🥇 | 30 ms |
| primes | trial-division | 20 k | 87 ms | 346 ms | **21 ms** 🥇 | 26 ms |
| collatz | tight integer loop | 30 k | 1.10 s | 376 ms | 228 ms | **32 ms** 🥇 |
| mandelbrot | floating-point | 128 | 352 ms | 386 ms | 76 ms | **26 ms** 🥇 |
| matmul | nested loops + indexing | 80 | 795 ms | 333 ms | 53 ms | **24 ms** 🥇 |
| strings | string building | 50 k | 237 ms | 331 ms | **17 ms** 🥇 | 29 ms |
| wordcount | hash-map build | 100 k | 609 ms | 336 ms | **30 ms** 🥇 | 32 ms |
| bintree | allocation / GC | 40 | 472 ms | 347 ms | 30 ms | **29 ms** 🥇 |
| sort | sort + checksum walk | 50 k | 122 ms | 305 ms | **29 ms** 🥇 | 38 ms |
| spawn | 20 k lightweight processes | 20 k | 613 ms | **344 ms** 🥇 | — | — |
| pfib | 100 fibs **in parallel** | 28 | 3.84 s | 366 ms | 294 ms | **130 ms** 🥇 |
| http | 500 **concurrent** HTTP GETs | 500 | 188 ms | 615 ms | 225 ms | **152 ms** 🥇 |

The single-threaded compute rows are where the inlining release moved: `fib` 824
→ 361 ms, `loop` 1.06 s → 426 ms, `primes` 160 → 87 ms, `collatz` 1.95 → 1.10 s,
`matmul` 1.19 s → 795 ms, `bintree` 691 → 472 ms — all from running the hot
arithmetic and comparison operators inline instead of dispatching a call for each
one. The newest change is to **parallel** memory, not single-thread speed: a
process-count-aware GC floor cut `pfib`'s peak ~10× (see below).

---

## Memory & startup — where Brood is light

| | cold start | memory at rest |
|---|---:|---:|
| Python | **11 ms** 🥇 | 10 MB |
| Node | 21 ms | 45 MB |
| Brood | 24 ms | **11 MB** |
| Elixir | 322 ms | 92 MB |

Memory is the durable win: Brood holds **11–37 MB** for most workloads — a
fraction of Elixir's 90–115 MB and well under Node's 44–69 MB — and stays
essentially tied with Python for lightest at rest. Startup is ~24 ms: Python
and Node edge it by a few ms, but it's still ~13× ahead of Elixir's BEAM, which
spends a third of a second warming up. For short-lived work that's why Brood
still beats Elixir end-to-end on the quick tasks (`primes`, `sort`, `strings`):
the BEAM's compiled code is fast, but Brood has finished before it's ready.

The exception is **`reduce`** (139 MB): `(range 1_000_000)` builds the whole
list in memory, where the others stream it. It's the one workload where Brood is
heavier than every competitor — worth knowing if you materialize large
sequences.

## Raw compute — slower than a JIT, but the gap narrowed

When the work is a tight loop running inside the language, Brood still trails —
but a lot less than it used to. With the core operators now inlined, `collatz`
≈ 1.1 s, `matmul` ≈ 0.79 s, `loop` ≈ 0.43 s, `fib` ≈ 0.37 s — roughly **12–35×
slower than Node**, whose JIT compiles to native code (down from 25–90× on the
previous VM), and 2–15× behind Python. Note that most of **Elixir's** numbers
here are just BEAM boot (~320 ms); its actual compute is fast — its wall time is
the price of starting, which amortizes away in a long-running service.

If your hot path is number-crunching, Brood is still not the fastest tool — or
push that work into a Rust-backed builtin (`sort` is Brood's best compute result,
123 ms, because the sorting itself isn't interpreted). But the inlining means the
interpreter tax on ordinary arithmetic-heavy code is now a small-tens multiple of
a JIT, not two orders of magnitude.

## Parallel CPU work (`pfib`) — slow, but no longer memory-hungry

`pfib` computes `fib(28)` **100 times at once**, each language using its
idiomatic parallelism (Brood/Elixir spawn lightweight processes; Node uses
`worker_threads`; Python uses `multiprocessing`).

| lang | wall | peak RSS |
|---|---:|---:|
| node | **130 ms** 🥇 | 315 MB |
| python | 294 ms | **22 MB** 🥇 |
| elixir | 366 ms | 96 MB |
| brood | 3.84 s | 102 MB |

Two honest takeaways. **Parallelism does help Brood** — the multicore scheduler
genuinely spreads the work across cores. But **each `fib` is interpreter-bound**,
so Brood starts from a per-task cost well above a JIT, and parallelism can't close
that: it's last on wall time and that's inherent to racing a JIT 100 ways at once.

**The memory, though, used to be the bigger embarrassment — and it's now fixed.**
This row peaked at **~980 MB** in earlier rounds: each share-nothing process built
up to its single-process GC floor (~64K objects) before its first collection, so
100 churny processes each climbed to a multi-MB heap at once. A
**process-count-aware GC floor** (the runtime now divides that object budget
across the live processes, so a wide fan-out collects earlier) brought the peak
down to **~102 MB — in line with Elixir (96 MB) and a third of Node's (315 MB)** —
with no wall-time cost (it's actually slightly faster, since the collections that
were happening anyway now keep working sets cache-resident). A lone process is
unchanged. So: still the wrong tool for parallel number-crunching on *speed*, but
no longer a memory outlier. (This row is also the most load-sensitive in the
suite, since it saturates every core.)

## Concurrent I/O (`http`) — Brood close behind Node

`http` fires **500 concurrent GETs** at a local server that sleeps 20 ms per
request, so it measures how well each runtime overlaps in-flight requests — pure
I/O concurrency, where raw compute speed barely matters.

| lang | wall | peak RSS |
|---|---:|---:|
| node | **152 ms** 🥇 | 70 MB |
| **brood** | 188 ms | 64 MB |
| python | 225 ms | 53 MB |
| elixir | 615 ms | 777 MB |

This is the mirror image of `pfib`. Brood's green processes **park** on the
response (its TCP is message-based), so all 500 requests are genuinely in flight
at once — and it lands **within ~25% of Node** (188 ms vs 152 ms), the runtime
whose event loop is built for exactly this, while using less memory, and ahead
of Python's thread pool. Elixir's *stdlib* `:httpc` is slow and heavy here (real
Elixir services use a third-party client like Finch). When your work is waiting
on I/O, Brood's concurrency model pays off.

## Lightweight processes (`spawn`)

Fanning out 20,000 processes that each send one message: Elixir is faster
end-to-end (344 ms vs 613 ms), but Brood does it in **37 MB vs Elixir's 108 MB**.
Cheap, plentiful processes are a real part of the runtime — note how different
this is from `pfib`: 20,000 *tiny* processes are cheap; 100 *compute-heavy* ones
are not.

---

## So when should I use Brood?

**A good fit:**

- Command-line tools and short-lived scripts — fast start, tiny footprint.
- Memory-constrained environments — a fraction of the BEAM's or Node's RAM.
- I/O-bound concurrency — many simultaneous requests/connections, where it's
  competitive with Node and far lighter than stdlib Elixir.

**A poor fit:**

- CPU-bound number crunching — interpreted loops are still a small-tens multiple
  off a JIT (better than before, but not close), parallel or not. Parallel
  fan-out is now memory-competitive (the `pfib` GC-floor fix), but still slow per
  task — use it for *I/O* concurrency, not *compute* fan-out.
- Materializing huge in-memory collections — see `reduce`.

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
0.1.0 (bytecode VM + primitive inlining + process-count-aware GC floor) · Elixir
1.20.0-rc.6 / OTP 29 · Python 3.14.4 · Node 24.15.0. Compute rows are best-of-3
from the full suite; the latency-sensitive `startup` and `http` rows are
best-of-5–7 measured in isolation so neighbouring benchmarks' load doesn't
inflate them. `pfib` saturates every core and remains the most load-sensitive
row in the suite._
