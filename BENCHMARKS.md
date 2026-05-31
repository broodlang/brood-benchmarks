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
> operations instead of through a dispatched call. Two recent runtime fixes show
> up below: a **process-count-aware GC floor** cut parallel fan-out's peak memory
> ~10× (`pfib` ~980 MB → ~100 MB), and **routing spawned processes through the
> VM** (they were tree-walked even under the VM) cut `pfib`'s *wall time* ~4.7×
> (3.84 s → 0.82 s). The numbers below are that engine.

## The honest summary

- **Memory — Brood's clear strength.** A ~11 MB base, holding 11–37 MB across
  most workloads, versus Elixir's 90–115 MB and Node's 44–69 MB. Startup is
  ~24 ms: not the fastest (Python and Node both edge it, within a few ms) but
  ~13× ahead of Elixir's BEAM, so Brood still finishes short tasks before the
  BEAM has booted.
- **Raw single-threaded compute — Brood's weakest area.** Its bytecode VM is
  young, and on tight loops it trails not just Node's JIT (**~12–35×**) but mature
  bytecode interpreters too: roughly **4–12× slower than Ruby** and **2–5× behind
  Python** (both interpreted, no JIT — so this isn't a JIT gap, it's headroom left
  in the VM). Primitive inlining narrowed it from the old tree-walker, but compute
  is where Brood pays.
- **Concurrency depends entirely on the workload.** Cheap, plentiful lightweight
  processes and **concurrent I/O** are a genuine strength (it lands within ~20%
  of Node on the HTTP test, ahead of Python and well ahead of Ruby). **Parallel
  CPU crunching** is now respectable too: two runtime fixes (below) took `pfib`
  from 30× off the pack and ~980 MB to **sub-second (0.82 s) and the lightest in
  the field (26 MB)** — still last on wall time, but by ~2–6×, not orders of
  magnitude. Both results are below.

---

## Full results — total wall time

The whole process, start to finish (startup + work). 🥇 marks the fastest in
each row. `N` is the workload size.

| benchmark | what it stresses | N | brood | elixir | python | node | ruby |
|-----------|------------------|--:|------:|-------:|-------:|-----:|-----:|
| startup | cold start + base memory | — | 24 ms | 327 ms | **15 ms** 🥇 | 24 ms | 43 ms |
| fib | deep recursion | 30 | 365 ms | 372 ms | 72 ms | **30 ms** 🥇 | 100 ms |
| loop | 3 M-iteration count | 3 M | 431 ms | 369 ms | 190 ms | **25 ms** 🥇 | 109 ms |
| reduce | fold over 1 M numbers | 1 M | 1.39 s | 346 ms | **18 ms** 🥇 | 27 ms | 44 ms |
| primes | trial-division | 20 k | 91 ms | 386 ms | **22 ms** 🥇 | 33 ms | 52 ms |
| collatz | tight integer loop | 30 k | 1.10 s | 369 ms | 232 ms | **31 ms** 🥇 | 134 ms |
| mandelbrot | floating-point | 128 | 352 ms | 366 ms | 77 ms | **26 ms** 🥇 | 70 ms |
| matmul | nested loops + indexing | 80 | 785 ms | 335 ms | 57 ms | **28 ms** 🥇 | 66 ms |
| strings | string building | 50 k | 218 ms | 332 ms | **22 ms** 🥇 | 34 ms | 54 ms |
| wordcount | hash-map build | 100 k | 614 ms | 318 ms | 29 ms | **29 ms** 🥇 | 51 ms |
| bintree | allocation / GC | 40 | 466 ms | 340 ms | 29 ms | **27 ms** 🥇 | 61 ms |
| sort | sort + checksum walk | 50 k | 124 ms | 342 ms | **28 ms** 🥇 | 42 ms | 52 ms |
| spawn | 20 k lightweight processes | 20 k | 632 ms | **388 ms** 🥇 | — | — | — |
| pfib | 100 fibs **in parallel** | 28 | 817 ms | 378 ms | 305 ms | **135 ms** 🥇 | 178 ms |
| http | 500 **concurrent** HTTP GETs | 500 | 238 ms | 641 ms | 227 ms | **201 ms** 🥇 | 422 ms |

Two recent runtime fixes show in these numbers. **`pfib` 3.84 s → 0.82 s**: a
spawned process's body was running on the *tree-walker* even under `BROOD_VM=1`
(the spawn entry didn't route through the VM), so every green process was ~4–5×
slower than the same code at top level; routing them through the VM closed that.
And **`pfib` peak ~980 MB → ~100 MB**: a process-count-aware GC floor (see that
section). Single-threaded compute is unchanged — that's the VM's standing speed,
and where Brood still trails the others.

---

## Memory & startup — where Brood is light

| | cold start | memory at rest |
|---|---:|---:|
| Python | **15 ms** 🥇 | 10 MB |
| Brood | 24 ms | **11 MB** |
| Node | 24 ms | 45 MB |
| Ruby | 43 ms | 23 MB |
| Elixir | 327 ms | 92 MB |

Memory is the durable win: Brood holds **11–37 MB** for most workloads — a
fraction of Elixir's 90–115 MB, well under Node's 44–69 MB, and lighter than
Ruby's steady ~23 MB — staying essentially tied with Python for lightest at rest.
Startup is ~24 ms: Python edges it, Node ties it, Ruby trails at ~43 ms, but it's
still ~13× ahead of Elixir's BEAM, which spends a third of a second warming up.
For short-lived work that's why Brood still beats Elixir end-to-end on the quick
tasks (`primes`, `sort`, `strings`): the BEAM's compiled code is fast, but Brood
has finished before it's ready.

The exception is **`reduce`** (139 MB): `(range 1_000_000)` builds the whole
list in memory, where the others stream it. It's the one workload where Brood is
heavier than every competitor — worth knowing if you materialize large
sequences.

## Raw compute — Brood's weakest area, and not just versus a JIT

When the work is a tight loop running inside the language, Brood trails everyone.
`collatz` ≈ 1.1 s, `matmul` ≈ 0.79 s, `loop` ≈ 0.43 s, `fib` ≈ 0.37 s — roughly
**12–35× slower than Node**, whose JIT compiles to native code. That much is
expected. The more telling comparison is **Ruby** (added this round) and
**Python**: both are bytecode interpreters with no JIT on by default, and both
still beat Brood — Ruby by **~4–12×** (`fib` 100 ms vs 365 ms, `matmul` 66 ms vs
785 ms), Python by ~2–5×. So this isn't a JIT gap; it's headroom left in a young
VM. Primitive inlining narrowed it from the old tree-walker, but the compute
engine has real distance to make up. (Most of **Elixir's** numbers here are just
BEAM boot ~320 ms; its actual compute is fast, and amortizes away in a
long-running service.)

If your hot path is number-crunching, Brood is not the tool yet — or push that
work into a Rust-backed builtin (`sort` is Brood's best compute result, 124 ms,
because the sorting itself isn't interpreted).

## Parallel CPU work (`pfib`) — fixed from a disaster to merely last

`pfib` computes `fib(28)` **100 times at once**, each language using its
idiomatic parallelism (Brood/Elixir spawn lightweight processes; Node uses
`worker_threads`; Python and Ruby fork a process pool).

| lang | wall | peak RSS |
|---|---:|---:|
| node | **135 ms** 🥇 | 334 MB |
| ruby | 178 ms | 23 MB |
| python | 305 ms | 22 MB |
| elixir | 378 ms | 99 MB |
| brood | 817 ms | **26 MB** 🥇 |

This row used to be Brood's worst result by far — **3.84 s and ~980 MB**. Two
runtime fixes turned it around:

- **Wall time (3.84 s → 0.82 s).** A spawned process's body was running on the
  **tree-walker even under `BROOD_VM=1`** — the `spawn` entry point called the
  tree-walk `apply`, not the VM — so every green process computed ~4–5× slower
  than the identical code at top level. Routing spawned bodies through the VM
  (with its inlined primitives) closed that gap; a single spawned `fib(28)` went
  from 0.66 s to 0.15 s, matching the root thread.
- **Memory (~980 MB → 26 MB).** Each share-nothing process climbed to its
  single-process GC floor (~64K objects) before its first collection; a
  **process-count-aware GC floor** now divides that budget across the live
  processes, so a wide fan-out collects earlier. Brood is now the **lightest in
  the field** on this benchmark (26 MB vs Node's 334 MB).

What's left is honest: Brood is **still last on wall time**, but by ~2–6×, not
30×, and now in the same league as the others — while using the least memory. The
remaining gap is the single-thread VM speed (above), not the scheduler, which
spreads the work across cores fine. (This row saturates every core, so it's the
most load-sensitive in the suite.)

## Concurrent I/O (`http`) — Brood runs with the front-runners

`http` fires **500 concurrent GETs** at a local server that sleeps 20 ms per
request, so it measures how well each runtime overlaps in-flight requests — pure
I/O concurrency, where raw compute speed barely matters.

| lang | wall | peak RSS |
|---|---:|---:|
| node | **201 ms** 🥇 | 70 MB |
| python | 227 ms | 46 MB |
| brood | 238 ms | 50 MB |
| ruby | 422 ms | 50 MB |
| elixir | 641 ms | 779 MB |

This is the mirror image of `pfib`. Brood's green processes **park** on the
response (its TCP is message-based), so all 500 requests are genuinely in flight
at once — and it lands in the **front group, ~18% behind Node** (238 ms vs
201 ms) and a hair behind Python's thread pool, while using the least memory of
the three. Ruby's thread-per-request (a fresh `Net::HTTP` connection each) is
heavier here, and Elixir's *stdlib* `:httpc` is slow and heavy (real Elixir
services use a third-party client like Finch). When your work is waiting on I/O,
Brood's concurrency model pays off. (This row is latency-sensitive and the
numbers bounce a bit run-to-run; the ordering is stable.)

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

- CPU-bound number crunching — the VM trails not just JITs but Ruby and Python
  too (~4–12× / ~2–5×). Parallel fan-out is no longer a disaster (sub-second and
  the lightest), but per-task compute is still the bottleneck — lean on Brood for
  *I/O* concurrency, not *compute* fan-out.
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
0.1.0 (bytecode VM + primitive inlining + process-count-aware GC floor +
VM-routed spawned processes) · Elixir 1.20.0-rc.6 / OTP 29 · Python 3.14.4 · Node
24.15.0 · Ruby 3.3.8. Compute rows are best-of-3 from the full suite; the
latency-sensitive `startup` and `http` rows are best-of-5 measured in isolation
so neighbouring benchmarks' load doesn't inflate them. `pfib` saturates every
core and remains the most load-sensitive row in the suite._
