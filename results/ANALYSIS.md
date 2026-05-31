# Where Brood is faster — and slower — than Elixir / Python / Node

Machine: Intel Raptor Lake-S (28 cores), 61 GB RAM, Ubuntu 26.04.
Runtimes: Brood 0.1.0 (bytecode VM) · Elixir 1.20.0-rc.6 / OTP 29 · Python 3.14.4 · Node 24.15.0.
Best of 3 runs. Full numbers + checksums in `report.md` / `results.json`.

> **Engine note:** Brood now runs on the **bytecode VM** (ADR-076), the
> closure-compiling engine that became the default and superseded the original
> tree-walker. It roughly **halved** every compute-bound wall time vs the
> tree-walker (~2×). The numbers below are the VM.

## 1. Startup & memory — Brood wins, decisively

| | wall | peak RSS |
|---|---|---|
| **brood**  | **9 ms** | **9.0 MB** |
| python | 12 ms | 9.6 MB |
| node   | 23 ms | 45 MB |
| elixir | 302 ms | 91 MB |

Brood starts in ~9 ms with the smallest footprint of the four — even edging out
Python, and ~33× faster than the BEAM. For short-lived CLI-style work this is
the single biggest differentiator. Brood's resident memory stays in the
9–27 MB range for almost every workload; Elixir sits at 90–112 MB throughout,
Node at 45–55 MB.

## 2. Raw single-threaded compute — Brood is slowest

Brood now runs on a **bytecode VM** (ADR-076), but it's still bytecode dispatch,
not native code — so anything that spends its time in *Brood code* (loops,
recursion, arithmetic) runs ~25–90× slower than the JIT (Node) and behind Python
and BEAM-compiled Elixir. (The VM roughly halved this gap vs the old tree-walker,
which was 50–190× off.)

The honest comparison against Elixir has to **subtract startup**, because at
these sizes Elixir's wall time is almost entirely BEAM boot. Compute-only
(wall − each runtime's own startup), in milliseconds:

| benchmark | brood | elixir | python | node |
|-----------|------:|-------:|-------:|-----:|
| fib        | 819 | 65 | 65 | 10 |
| loop       | 1042 | 51 | 172 | 3 |
| reduce     | 1766 | ~1* | 7 | 2 |
| primes     | 153 | 45 | 8 | 3 |
| collatz    | 1995 | 67 | 221 | 8 |
| mandelbrot | 430 | 94 | 70 | 2 |
| matmul     | 1174 | 25 | 44 | 1 |
| strings    | 242 | 73 | 5 | 6 |
| wordcount  | 548 | 67 | 20 | 5 |
| bintree    | 682 | 92 | 17 | 4 |
| sort       | 115 | 85 | 18 | 18 |

`*` within startup-measurement noise — BEAM compute is essentially free at this size.

Takeaways:

- **Node's JIT dominates pure compute** everywhere.
- **Elixir's *compute* is excellent** — frequently faster than Python (loop,
  collatz, matmul, strings). Its big wall-clock numbers are the 325 ms BEAM
  boot, not slow execution. For a long-running service that cost amortises to
  zero; for a one-shot script it dominates.
- **Brood's gap shrinks dramatically when the work lives in a Rust builtin.**
  `sort` is its best result (124 ms, only ~4× the fastest, beating Elixir's
  wall) because the comparison sort runs in Rust, not the VM. The lesson for
  Brood code: push hot work into builtins (`sort`, `reduce`, string ops) and keep
  hand-written loops shallow. `primes` and `strings` also now beat Elixir
  end-to-end.

## 3. Immutable data has a visible memory cost

- `reduce` over `(range 1_000_000)` makes Brood materialise a million-element
  list → **139 MB** peak (vs ~9 MB for the others, which stream the range).
  A transducer or a tail-recursive counter would avoid the allocation; the naive
  combinator pays for it.
- `strings` (build via `join`) hits 33 MB in Brood vs 13 MB in Python.
- Elsewhere Brood's persistent maps/vectors stay cheap (`wordcount` 27 MB, `sort`
  19 MB, `matmul` 18 MB; the allocation-free loops sit at ~9 MB) — immutability
  is not *inherently* costly, but whole-collection materialisation is.

## 4. Concurrency — Brood holds its own against the BEAM

`spawn`: fan out N=20 000 lightweight processes, each sends one message back.

| | wall | peak RSS |
|---|---|---|
| elixir | 370 ms | 112 MB |
| **brood**  | 622 ms | **32.4 MB** |

Elixir is faster end-to-end, but Brood spawns and message-passes 20 000 green
processes in the same order of magnitude while using **~3.5× less memory** — and
at smaller N (5 000) Brood was actually *faster* than Elixir. Green processes
are a genuine strength of the Brood runtime, not just the BEAM's. (No Python/Node
entry: OS threads / an event loop aren't a like-for-like comparison.)

## Bottom line

- **Use Brood where startup latency and memory footprint matter** — short-lived
  CLI tools, scripts, spawn-heavy concurrent workloads on a memory budget. It
  boots faster and lighter than everything here, the BEAM especially.
- **Don't reach for Brood for compute-bound number-crunching** — even on the
  bytecode VM, tight loops are ~1–2 orders of magnitude off Node and still behind
  Python. Lean on Rust builtins for the hot path.
- **vs Elixir specifically:** Brood wins startup and memory by a wide margin, now
  beats Elixir end-to-end on four short benchmarks (`startup`, `primes`,
  `strings`, `sort`), and is competitive on concurrency; Elixir wins raw
  execution speed once its VM is warm. They're optimised for different points —
  Brood for fast/light one-shots, the BEAM for long-running concurrent services.
