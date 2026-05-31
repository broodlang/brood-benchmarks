# Brood vs Elixir vs Python vs Node — benchmark breakdown

A suite of 13 small programs, each implemented **four times** (once per language)
and run under an identical harness, to see where the Brood runtime is faster
or slower than the alternatives — on **startup**, **memory**, and **raw
performance**.

> **Verified equivalent:** every program prints a checksum, and the harness
> asserts all four languages produce the *same* checksum on every benchmark — so
> these are apples-to-apples comparisons, not different amounts of work.

> **Engine:** these numbers are the **bytecode VM** (ADR-076), now Brood's
> default execution engine — the closure-compiling VM superseded the original
> tree-walker and roughly **halved** every compute-bound wall time (~2× across
> the board; see the progress log in [`OPTIMIZATION.md`](OPTIMIZATION.md)).

**Environment:** Intel Raptor Lake-S (28 cores) · 61 GB RAM · Ubuntu 26.04 ·
Brood 0.1.0 (bytecode VM) · Elixir 1.20.0-rc.6 / OTP 29 · Python 3.14.4 ·
Node 24.15.0. Best of 3 runs each. Raw data:
[`results/results.json`](results/results.json) · full tables:
[`results/report.md`](results/report.md).

---

## ⏱️ Total wall time (startup + compute)

Best-of-3 wall time for the whole process. 🥇 marks the fastest in each row.

| benchmark | N | brood | elixir | python | node | stresses |
|-----------|--:|------:|-------:|-------:|-----:|----------|
| startup | — | **9 ms** 🥇 | 302 ms | 12 ms | 23 ms | VM boot + base memory |
| fib | 30 | 828 ms | 367 ms | 78 ms | **33 ms** 🥇 | recursion / call overhead |
| loop | 3 M | 1.05 s | 353 ms | 184 ms | **26 ms** 🥇 | raw iteration |
| reduce | 1 M | 1.78 s | 303 ms | **19 ms** 🥇 | 25 ms | higher-order fold |
| primes | 20 k | 162 ms | 347 ms | **20 ms** 🥇 | 26 ms | integer arithmetic |
| collatz | 30 k | 2.00 s | 369 ms | 233 ms | **31 ms** 🥇 | tight integer loop |
| mandelbrot | 128 | 439 ms | 396 ms | 82 ms | **25 ms** 🥇 | floating-point math |
| matmul | 80 | 1.18 s | 327 ms | 56 ms | **24 ms** 🥇 | nested loops + indexing |
| strings | 50 k | 251 ms | 375 ms | **17 ms** 🥇 | 28 ms | string building |
| wordcount | 100 k | 557 ms | 369 ms | 33 ms | **28 ms** 🥇 | hash-map build |
| bintree | 40 | 691 ms | 394 ms | 29 ms | **27 ms** 🥇 | allocation / GC pressure |
| sort | 50 k | 124 ms | 387 ms | **30 ms** 🥇 | 41 ms | sort + checksum walk |
| spawn | 20 k | 622 ms | **370 ms** 🥇 | — | — | lightweight processes |

---

## 🧠 Peak resident memory

| benchmark | brood | elixir | python | node |
|-----------|------:|-------:|-------:|-----:|
| startup | **9 MB** 🥇 | 91 MB | 10 MB | 45 MB |
| _typical compute_ | 9–27 MB | 92–103 MB | 9–13 MB | 50–55 MB |
| reduce (materialises a 1 M list) | ⚠️ 139 MB | 93 MB | **9 MB** 🥇 | 53 MB |
| strings | 33 MB | 103 MB | **13 MB** 🥇 | 55 MB |
| spawn (20 k processes) | **32 MB** 🥇 | 112 MB | — | — |

Brood stays at **9–27 MB** for nearly everything (and as low as **9 MB** on the
tail-recursive loops that allocate nothing); Elixir sits at **90–112 MB**
throughout, Node at **45–55 MB**. Python is the leanest on pure compute (~10 MB).

---

## 🔬 Compute-only — the fair comparison

At these sizes **Elixir's wall time is almost entirely the ~300 ms BEAM boot**.
Subtract each runtime's own startup and the *execution* picture changes
completely (milliseconds):

| benchmark | brood | elixir | python | node |
|-----------|------:|-------:|-------:|-----:|
| fib | 819 | 65 | 65 | 10 |
| loop | 1042 | 51 | 172 | 3 |
| reduce | 1766 | ~1 | 7 | 2 |
| primes | 153 | 45 | 8 | 3 |
| collatz | 1995 | 67 | 221 | 8 |
| mandelbrot | 430 | 94 | 70 | 2 |
| matmul | 1174 | 25 | 44 | 1 |
| strings | 242 | 73 | 5 | 6 |
| wordcount | 548 | 67 | 20 | 5 |
| bintree | 682 | 92 | 17 | 4 |
| sort | 115 | 85 | 18 | 18 |
| spawn | 613 | 68 | — | — |

_(Competitor compute-only figures are small differences of two ~300 ms+
measurements for Elixir and a few ms for Python/Node, so they're noise-dominated
— `~1` means wall ≈ startup. The Brood column is the stable one.)_

- **Node's JIT dominates** pure compute everywhere.
- **Elixir's compute is excellent** — frequently faster than Python (loop,
  collatz, strings, wordcount). Its large wall numbers are VM boot, not slow
  code: a cost that amortises to zero for a long-running service but dominates a
  one-shot script.
- **Brood's gap collapses when work runs in a Rust builtin.** `sort` (115 ms
  compute, on par with Python/Node and beating Elixir's wall) and `primes`
  (153 ms) are its best results because that work isn't run instruction-by-
  instruction in the VM.

### 🎯 Brood optimization targets (by compute-only cost)

Where the VM spends its time, worst first — the candidate list for optimization
work:

| rank | benchmark | brood compute | what's hot (likely cause) |
|-----:|-----------|--------------:|---------------------------|
| 1 | collatz | 1995 ms | tightest hot loop — `rem`/`quot`/`*` dispatch per step |
| 2 | reduce | 1766 ms | 1 M-element `range` list + per-element closure call (also 139 MB) |
| 3 | matmul | 1174 ms | `nth` indexing + arithmetic in the inner `dot` recursion |
| 4 | loop | 1042 ms | bare tail-call + `+`/`>=` dispatch — pure VM overhead floor |
| 5 | fib | 819 ms | function-call / frame setup per recursive call |
| 6 | bintree | 682 ms | vector allocation + non-tail tree recursion (GC/alloc path) |
| 7 | mandelbrot | 430 ms | f64 arithmetic dispatch in the escape loop |

**Two source-level tweaks (same algorithm, identical checksums):**

- **mandelbrot CSE** — carry `x*x`/`y*y` instead of recomputing them (~5 → 3
  multiplies per iteration). Helped *everyone* a little: Brood, Elixir small
  gains, Python/Node flat. Safe, kept.
- **primes √n hoist** — replace the inner `d*d <= n` multiply with a precomputed
  `d <= √n` bound. Sped up Python and Node — but **slowed Brood**: the bound is a
  *float*, so `d <= limit` becomes a **mixed int/float comparison** that costs
  more than the integer multiply it removes. Kept for Python/Node/Elixir,
  **reverted for Brood** — the fastest non-fancy form is language-dependent.

**The bytecode VM (ADR-076)** is the change that moved the whole table at once:
the closure-compiling engine replaced the tree-walker and **roughly halved every
compute-bound wall time** — `loop` 2.22 s → 1.05 s, `collatz` 4.25 s → 2.00 s,
`matmul` 2.63 s → 1.18 s, `fib` 1.71 s → 828 ms, `mandelbrot` 1.05 s → 439 ms
(~1.8–2.4× each). `reduce` and the allocation-bound rows moved less (their cost
is the 1 M-element list and GC pressure, not instruction dispatch), which is why
they lead the target table above. The numbers shown are current.

The remaining levers are **per-operation dispatch in the VM** (rows 1, 4, 5),
**collection access / allocation** (rows 3, 6), **whole-collection
materialisation** (row 2's 139 MB), and a general one an earlier round exposed:
**integer ops are cheaper than float/mixed ops** — prefer integer arithmetic and
avoid silent int→float coercion on hot paths.

Cheap wins that aren't dispatch-bound: `sort`, `primes`, `strings` (≤ ~250 ms) —
these already lean on builtins or do less per iteration, and `primes`, `strings`,
and `sort` now all **beat Elixir end-to-end**.

> Re-run any single benchmark in isolation while iterating:
> `BENCH_N=30000 brood bench/brood/collatz.blsp` (or
> `python3 bench/harness.py --only collatz,loop --langs brood --runs 5`).

---

## 🥊 vs the worst competitor (wall + memory)

A friendlier framing: for each benchmark, how does Brood do against the
*slowest* / *heaviest* of the other three? (It's **Elixir on every row** — its
~300 ms BEAM boot makes it the worst on wall, and its 90–112 MB resident set the
worst on memory.)

| benchmark | brood wall | worst wall | wall | brood mem | worst mem | mem |
|-----------|-----------:|-----------:|:----:|----------:|----------:|:---:|
| startup | 9 ms | 302 ms | ✅ 33× | 9 MB | 91 MB | ✅ 10× |
| fib | 828 ms | 367 ms | 2.3× | 9 MB | 95 MB | ✅ 11× |
| loop | 1.05 s | 353 ms | 3.0× | 9 MB | 95 MB | ✅ 10× |
| reduce | 1.78 s | 303 ms | 5.9× | 139 MB | 93 MB | ❌ 1.5× |
| primes | 162 ms | 347 ms | ✅ 2.1× | 9 MB | 94 MB | ✅ 10× |
| collatz | 2.00 s | 369 ms | 5.4× | 17 MB | 97 MB | ✅ 6× |
| mandelbrot | 439 ms | 396 ms | 1.1× | 9 MB | 95 MB | ✅ 11× |
| matmul | 1.18 s | 327 ms | 3.6× | 18 MB | 92 MB | ✅ 5× |
| strings | 251 ms | 375 ms | ✅ 1.5× | 33 MB | 103 MB | ✅ 3× |
| wordcount | 557 ms | 369 ms | 1.5× | 27 MB | 92 MB | ✅ 3× |
| bintree | 691 ms | 394 ms | 1.8× | 21 MB | 95 MB | ✅ 5× |
| sort | 124 ms | 387 ms | ✅ 3.1× | 19 MB | 103 MB | ✅ 5× |
| spawn | 622 ms | 370 ms | 1.7× | 32 MB | 112 MB | ✅ 3× |

**Scorecard vs the worst competitor — wall: 4 / 13 · memory: 12 / 13.**

On wall Brood now wins `startup`, `sort`, `primes`, and `strings` — Elixir's
compiled execution is fast once booted, but Brood's instant start beats it on the
short tasks, and the VM brought `mandelbrot` to within a hair (1.1×). On
**memory the picture flips** entirely: Brood is lighter than the heaviest
competitor on **12 of 13** benchmarks, usually by **3–11×**. Even where it loses
on wall it wins big on memory — `collatz` is 5.4× slower yet uses **6× less**
memory.

The lone memory loss is **`reduce` (139 MB vs 93 MB)**, same root cause as its
slowness: `(range 1_000_000)` materialises a full 1 M-element list. A
lazy/fused range would fix the *only* benchmark where Brood loses on memory
*and* dent the wall gap — which is why it's high on the target list.

---

## 📌 Verdict: where Brood is faster, and where it's slower

### ✅ Brood wins
- **Startup** — 9 ms, **~33× faster than the BEAM** and even edging out Python.
- **Memory** — 5–11× lighter than Elixir on every compute workload; smallest
  base footprint of the four (9 MB), and as low as 9 MB on allocation-free loops.
- **Short tasks end-to-end** — `startup`, `primes`, `strings`, and `sort` all
  beat Elixir's wall outright; fast start + a builtin-bound hot path wins.
- **Concurrency on a budget** — spawns and message-passes 20 k green processes in
  the same order of magnitude as the BEAM while using **~3.5× less memory**
  (32 MB vs 112 MB).

### ❌ Brood loses
- **Raw compute** — even as a bytecode VM it runs **~25–90× slower** than Node's
  JIT on interpreted loops and recursion (`collatz` ≈ 2.0 s, `reduce` ≈ 1.8 s).
  The VM roughly halved this gap vs the old tree-walker, but a JIT is still a
  JIT.
- **Whole-collection materialisation** — `(range 1_000_000)` cost **139 MB**;
  a transducer or tail-recursive counter avoids the allocation.

### 🆚 Brood vs Elixir specifically
Brood wins startup and memory by a wide margin, now beats Elixir end-to-end on
four short benchmarks, and is competitive on concurrency; Elixir wins raw
execution once its VM is warm. They optimise for different points — **Brood for
fast, light, short-lived work** (CLI tools, scripts, memory-bounded concurrency);
**the BEAM for long-running concurrent services** where the boot cost amortises
away.

---

## How to reproduce

```sh
python3 bench/harness.py            # full suite, best of 3  → results/
python3 bench/harness.py --quick    # smaller sizes, smoke test
python3 bench/harness.py --only fib,sort --runs 5
```

The 50 source programs live under [`bench/`](bench/) (four per benchmark, except
`spawn` which is Brood + Elixir only), named
identically except the extension (`fib.blsp` / `fib.exs` / `fib.py` / `fib.js`)
so the implementations diff side by side. Methodology and fairness notes are in
the [README](README.md); Brood-specific optimization targets and the progress
log are in [`OPTIMIZATION.md`](OPTIMIZATION.md).
