# Where Brood is faster — and slower — than Elixir / Python / Node

Machine: Intel Raptor Lake-S (28 cores), 61 GB RAM, Ubuntu 26.04.
Runtimes: Brood 0.1.0 · Elixir 1.20.0-rc.6 / OTP 29 · Python 3.14.4 · Node 24.15.0.
Best of 3 runs. Full numbers + checksums in `report.md` / `results.json`.

## 1. Startup & memory — Brood wins, decisively

| | wall | peak RSS |
|---|---|---|
| **brood**  | **10 ms** | **8.7 MB** |
| python | 13 ms | 9.4 MB |
| node   | 22 ms | 45 MB |
| elixir | 325 ms | 91 MB |

Brood starts in ~10 ms with the smallest footprint of the four — even edging out
Python, and ~30× faster than the BEAM. For short-lived CLI-style work this is
the single biggest differentiator. Brood's resident memory stays in the
15–25 MB range for almost every workload; Elixir sits at 90–110 MB throughout,
Node at 45–55 MB.

## 2. Raw single-threaded compute — Brood is slowest

Brood is a **tree-walking interpreter**, so anything that spends its time in
*interpreted Brood code* (loops, recursion, arithmetic) runs 50–190× slower than
the JIT (Node) and well behind Python and BEAM-compiled Elixir.

The honest comparison against Elixir has to **subtract startup**, because at
these sizes Elixir's wall time is almost entirely BEAM boot. Compute-only
(wall − each runtime's own startup), in milliseconds:

| benchmark | brood | elixir | python | node |
|-----------|------:|-------:|-------:|-----:|
| fib        | 2390 | 63 | 61 | 7 |
| loop       | 3618 | 22 | 175 | 4 |
| reduce     | 4906 | 40 | 36 | 5 |
| primes     | 469 | 61 | 8 | 6 |
| collatz    | 5894 | 62 | 225 | 9 |
| mandelbrot | 1701 | 63 | 64 | 7 |
| matmul     | 3617 | ~0* | 40 | 3 |
| strings    | 585 | ~1* | 6 | 9 |
| wordcount  | 604 | 33 | 19 | 6 |
| bintree    | 1468 | 41 | 17 | 8 |
| sort       | 202 | 42 | 16 | 16 |

`*` within startup-measurement noise — BEAM compute is essentially free at this size.

Takeaways:

- **Node's JIT dominates pure compute** everywhere.
- **Elixir's *compute* is excellent** — frequently faster than Python (loop,
  collatz, matmul, strings). Its big wall-clock numbers are the 325 ms BEAM
  boot, not slow execution. For a long-running service that cost amortises to
  zero; for a one-shot script it dominates.
- **Brood's gap shrinks dramatically when the work lives in a Rust builtin.**
  `sort` is its best result (202 ms, only ~7× the fastest, beating Elixir's
  wall) because the comparison sort runs in Rust, not the interpreter. The
  lesson for Brood code: push hot work into builtins (`sort`, `reduce`, string
  ops) and keep hand-written interpreted loops shallow.

## 3. Immutable data has a visible memory cost

- `reduce` over `(range 1_000_000)` makes Brood materialise a million-element
  list → **245 MB** peak (vs ~10 MB for the others, which stream the range).
  A transducer or a tail-recursive counter would avoid the allocation; the naive
  combinator pays for it.
- `strings` (build via `join`) hits 70 MB in Brood vs 12 MB in Python.
- Elsewhere Brood's persistent maps/vectors stay cheap (`wordcount`, `sort`,
  `matmul` all ~20 MB) — immutability is not *inherently* costly, but
  whole-collection materialisation is.

## 4. Concurrency — Brood holds its own against the BEAM

`spawn`: fan out N=20 000 lightweight processes, each sends one message back.

| | wall | peak RSS |
|---|---|---|
| elixir | 382 ms | 111 MB |
| **brood**  | 654 ms | **29.5 MB** |

Elixir is faster end-to-end, but Brood spawns and message-passes 20 000 green
processes in the same order of magnitude while using **~4× less memory** — and
at smaller N (5 000) Brood was actually *faster* than Elixir. Green processes
are a genuine strength of the Brood runtime, not just the BEAM's. (No Python/Node
entry: OS threads / an event loop aren't a like-for-like comparison.)

## Bottom line

- **Use Brood where startup latency and memory footprint matter** — short-lived
  CLI tools, scripts, spawn-heavy concurrent workloads on a memory budget. It
  boots faster and lighter than everything here, the BEAM especially.
- **Don't reach for Brood for compute-bound number-crunching** — tight
  interpreted loops are 1–2 orders of magnitude off Node/Python. Lean on Rust
  builtins for the hot path.
- **vs Elixir specifically:** Brood wins startup and memory by a wide margin and
  is competitive on concurrency; Elixir wins raw execution speed once its VM is
  warm. They're optimised for different points — Brood for fast/light one-shots,
  the BEAM for long-running concurrent services.
