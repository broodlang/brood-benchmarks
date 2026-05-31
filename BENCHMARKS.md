# What to expect from Brood — benchmark results

Fifteen small programs, each written **four times** — in Brood, Elixir, Python,
and Node — and run under one identical harness. The goal isn't to crown a winner;
it's to give an honest, realistic picture of what you get with Brood and where
it costs you, measured against three well-known runtimes.

> Every program prints a checksum, and the harness verifies **all four languages
> produce the same answer** on every benchmark — so this is the same work, four
> ways, not different amounts of it.

> **Engine:** Brood runs on its bytecode VM (the closure-compiling engine that
> replaced the original tree-walker and roughly halved compute-bound times). The
> numbers below are that VM.

## The honest summary

- **Startup & memory — Brood's clear strengths.** ~11 ms cold start and a ~9 MB
  base; it stays far lighter than Elixir and Node across most workloads.
- **Raw single-threaded compute — expect to be slower.** As a bytecode
  interpreter, tight loops and recursion run roughly 25–90× slower than Node's
  JIT, and behind Python too. Short tasks still finish ahead of Elixir because
  Brood starts instantly.
- **Concurrency depends entirely on the workload.** Cheap, plentiful lightweight
  processes and **concurrent I/O** are a genuine strength (it lands within ~9%
  of Node on the HTTP test). **Parallel CPU crunching is not** — there it's slow *and*
  memory-hungry. Both results are below; the difference is the point.

---

## Full results — total wall time

The whole process, start to finish (startup + work). 🥇 marks the fastest in
each row. `N` is the workload size.

| benchmark | what it stresses | N | brood | elixir | python | node |
|-----------|------------------|--:|------:|-------:|-------:|-----:|
| startup | cold start + base memory | — | **11 ms** 🥇 | 353 ms | 12 ms | 27 ms |
| fib | deep recursion | 30 | 824 ms | 447 ms | 73 ms | **33 ms** 🥇 |
| loop | 3 M-iteration count | 3 M | 1.06 s | 333 ms | 184 ms | **24 ms** 🥇 |
| reduce | fold over 1 M numbers | 1 M | 1.79 s | 321 ms | **18 ms** 🥇 | 27 ms |
| primes | trial-division | 20 k | 160 ms | 395 ms | **20 ms** 🥇 | 24 ms |
| collatz | tight integer loop | 30 k | 1.95 s | 383 ms | 229 ms | **33 ms** 🥇 |
| mandelbrot | floating-point | 128 | 433 ms | 395 ms | 80 ms | **30 ms** 🥇 |
| matmul | nested loops + indexing | 80 | 1.19 s | 332 ms | 54 ms | **24 ms** 🥇 |
| strings | string building | 50 k | 249 ms | 326 ms | **16 ms** 🥇 | 31 ms |
| wordcount | hash-map build | 100 k | 545 ms | 340 ms | **30 ms** 🥇 | 32 ms |
| bintree | allocation / GC | 40 | 691 ms | 385 ms | 31 ms | **27 ms** 🥇 |
| sort | sort + checksum walk | 50 k | 123 ms | 357 ms | **30 ms** 🥇 | 37 ms |
| spawn | 20 k lightweight processes | 20 k | 613 ms | **378 ms** 🥇 | — | — |
| pfib | 100 fibs **in parallel** | 28 | 3.99 s | 394 ms | 304 ms | **132 ms** 🥇 |
| http | 500 **concurrent** HTTP GETs | 500 | 235 ms | 606 ms | 325 ms | **215 ms** 🥇 |

---

## Startup & memory — where Brood is strong

| | cold start | memory at rest |
|---|---:|---:|
| **Brood** | **11 ms** 🥇 | **9 MB** 🥇 |
| Python | 12 ms | 10 MB |
| Node | 27 ms | 45 MB |
| Elixir | 353 ms | 92 MB |

Brood boots in ~11 ms — edging out Python and ~32× faster than Elixir's BEAM,
which spends a third of a second warming up. On memory it holds **9–27 MB** for
most workloads, versus Elixir's 90–112 MB and Node's 45–56 MB. For short-lived
work — CLI tools, scripts — this is the differentiator, and it's why Brood beats
Elixir end-to-end on the short tasks (`startup`, `primes`, `sort`, `strings`):
Elixir's compiled code is fast, but Brood has already finished before the BEAM is
ready.

The exception is **`reduce`** (139 MB): `(range 1_000_000)` builds the whole
list in memory, where the others stream it. It's the one workload where Brood is
heavier than every competitor — worth knowing if you materialize large
sequences.

## Raw compute — where Brood is slow

When the work is a tight loop running inside the language, expect Brood to trail
badly: `collatz` ≈ 1.9 s, `matmul` ≈ 1.2 s, `loop` ≈ 1.0 s — roughly **25–90×
slower than Node**, whose JIT compiles to native code, and behind Python too.
The bytecode VM roughly halved this versus the old engine, but an interpreter
won't catch a JIT. Note that most of **Elixir's** numbers here are just BEAM
boot (~325 ms); its actual compute is fast — its wall time is the price of
starting, which amortizes away in a long-running service.

If your hot path is number-crunching, Brood is the wrong tool — or push that
work into a Rust-backed builtin (`sort` is Brood's best compute result, 123 ms,
because the sorting isn't interpreted).

## Parallel CPU work (`pfib`) — slow *and* memory-hungry

`pfib` computes `fib(28)` **100 times at once**, each language using its
idiomatic parallelism (Brood/Elixir spawn lightweight processes; Node uses
`worker_threads`; Python uses `multiprocessing`).

| lang | wall | peak RSS |
|---|---:|---:|
| node | **132 ms** 🥇 | 319 MB |
| python | 304 ms | **22 MB** 🥇 |
| elixir | 394 ms | 96 MB |
| brood | 3.99 s | 954 MB |

Two honest takeaways. **Parallelism does help Brood** — 100×`fib(28)` in 4 s
versus ~32 s sequential is a ~7× speedup across cores; the multicore scheduler
works. But **each `fib` is interpreter-bound**, so Brood starts from a per-task
cost two orders of magnitude above a JIT, and parallelism can't close that. And
because Brood processes are share-nothing — each carries its own ~9 MB heap —
**100 compute-heavy processes cost ~950 MB**. Parallel number-crunching is not
what Brood is for.

## Concurrent I/O (`http`) — Brood ties Node

`http` fires **500 concurrent GETs** at a local server that sleeps 20 ms per
request, so it measures how well each runtime overlaps in-flight requests — pure
I/O concurrency, where raw compute speed barely matters.

| lang | wall | peak RSS |
|---|---:|---:|
| node | **215 ms** 🥇 | 69 MB |
| **brood** | 235 ms | 65 MB |
| python | 325 ms | 49 MB |
| elixir | 606 ms | 782 MB |

This is the mirror image of `pfib`. Brood's green processes **park** on the
response (its TCP is message-based), so all 500 requests are genuinely in flight
at once — and it lands **within a hair of Node** (235 ms vs 215 ms), the runtime
whose event loop is built for exactly this. Python's thread pool is solid; Elixir's *stdlib* `:httpc` is
slow and heavy here (real Elixir services use a third-party client like Finch).
When your work is waiting on I/O, Brood's concurrency model pays off.

## Lightweight processes (`spawn`)

Fanning out 20,000 processes that each send one message: Elixir is faster
end-to-end (378 ms vs 613 ms), but Brood does it in **31 MB vs Elixir's 110 MB**.
Cheap, plentiful processes are a real part of the runtime — note how different
this is from `pfib`: 20,000 *tiny* processes are cheap; 100 *compute-heavy* ones
are not.

---

## So when should I use Brood?

**A good fit:**

- Command-line tools and short-lived scripts — instant start, tiny footprint.
- Memory-constrained environments — a fraction of the BEAM's or Node's RAM.
- I/O-bound concurrency — many simultaneous requests/connections, where it's
  competitive with Node and far lighter than stdlib Elixir.

**A poor fit:**

- CPU-bound number crunching — interpreted loops are 1–2 orders of magnitude off
  a JIT, parallel or not.
- Parallel compute fan-out — slow per task *and* heavy (one heap per process).
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

_Measured best-of-3 on: Intel Raptor Lake-S (28 cores) · 61 GB RAM · Ubuntu
26.04 · Brood 0.1.0 (bytecode VM) · Elixir 1.20.0-rc.6 / OTP 29 · Python 3.14.4 ·
Node 24.15.0._
