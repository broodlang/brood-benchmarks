# Things we can tackle — Brood performance opportunities

A working backlog for improving Brood's runtime, grounded in the benchmark
suite. Full methodology and the four-language comparison live in
[`BENCHMARKS.md`](BENCHMARKS.md); this doc is Brood-only: **the baseline to
beat**, **where the time/memory goes**, and **what to try next**.

All numbers are best-of-3, full sizes, current runtime. Re-measure after any
change with `python3 bench/harness.py --langs brood --runs 3` (or `--only <name>`
for one). Keep checksums identical — the harness verifies equivalent work.

---

## Baseline (current Brood vs the field)

`compute` = wall − Brood's own ~9 ms startup. `vs fastest` = Brood ÷ the fastest
of Elixir/Python/Node (≈ Node). `vs Elixir` = Brood ÷ Elixir wall (Elixir pays a
~310 ms boot, so beating it is the realistic short-term goal).

| benchmark | brood wall | compute | brood RSS | vs fastest | vs Elixir |
|-----------|-----------:|--------:|----------:|:----------:|:---------:|
| startup | 9 ms | 0 ms | 9 MB | ✅ win | ✅ win |
| sort | 164 ms | 155 ms | 24 MB | 6× | ✅ win |
| primes | 348 ms | 339 ms | 16 MB | 17× | ✅ win |
| strings | 488 ms | 479 ms | 40 MB | 30× | 1.5× |
| wordcount | 540 ms | 531 ms | 27 MB | 19× | 1.6× |
| spawn | 634 ms | 625 ms | 32 MB | 2× | 1.8× |
| mandelbrot | 1.05 s | 1040 ms | 20 MB | 42× | 2.9× |
| bintree | 1.24 s | 1235 ms | 28 MB | 47× | 3.4× |
| fib | 1.71 s | 1697 ms | 16 MB | 56× | 5.0× |
| loop | 2.22 s | 2209 ms | 16 MB | 77× | 6.1× |
| matmul | 2.63 s | 2618 ms | 19 MB | 105× | 8.5× |
| reduce | 3.54 s | 3531 ms | 125 MB ⚠️ | 205× | 11.4× |
| collatz | 4.25 s | 4237 ms | 16 MB | 134× | 11.9× |

**Scorecard vs the worst competitor (always Elixir): wall 3/13 · memory 12/13.**
Memory is already a strength (3–6× lighter than Elixir nearly everywhere); the
work is on **wall time of interpreted hot loops**, plus the **one memory
outlier** (`reduce`, 125 MB).

---

## Targets, in priority order

### 🥇 Tier 1 — highest leverage: eval-loop dispatch cost

**Evidence:** `loop` (103×), `collatz` (133×), `fib` (56×) are dominated by raw
per-operation interpreter overhead — `loop` does nothing but `(+ i 1)` /
`(>= i n)` and still costs 2.9 s for 3 M iterations (~1 µs/iter).

**Why it matters most:** every benchmark pays this tax, so cutting per-op
dispatch cost moves the *whole* table at once. The last runtime update already
took `loop` −11% — this is the seam that's paying off.

**Ideas to try:** tighter opcode/closure dispatch in the eval loop; avoid
re-resolving global symbols (`+`, `>=`) per call (cache the resolved fn on the
call site); specialise the 2-arg arithmetic/comparison path so variadic `+`/`<`
don't walk an argument list for the common binary case.

**Measure:** `--only loop,collatz,fib` and a Tier-3 micro-benchmark (below).

### 🥈 Tier 2 — collection access: `nth` on vectors

**Evidence:** `matmul` (125×) is `(nth (nth b k) j)` in its inner loop —
two indexes per multiply-add, 80³ = 512 k times.

**Check first:** confirm `nth` on a vector is genuinely O(1) and cheap, not a
bounds-check + generic-seq dispatch per call. If it's slow, a fast vector-index
path helps `matmul` and any indexed workload.

**Measure:** `--only matmul`; micro-bench a tight `(nth v i)` loop.

### 🥈 Tier 2 — allocation / GC: persistent vectors

**Evidence:** `bintree` (50×) builds and walks many small `[l r]` vectors;
`reduce`'s 125 MB is allocation too.

**Ideas:** faster small-vector allocation path or arena/freelist for short-lived
nodes; cheaper persistent-vector construction.

**Measure:** `--only bintree`; watch RSS as well as wall.

> **GC-tweak round (update 3) came out flat — and that's expected with this
> harness.** We measure **peak RSS** (`/usr/bin/time -v` high-water mark) and
> wall time. GC tuning mostly changes *allocation churn* and *pause time*, which
> don't move a peak-RSS number unless they change the live-set high point — and
> on these short, single-shot runs they don't surface in wall time either. To
> actually evaluate a GC change we need different instrumentation: **bytes
> allocated**, **collection count / total pause time**, or a long-lived
> allocation-churn workload — none of which the current suite exposes. If GC is a
> focus, the next harness addition should be an allocation/pause counter (or a
> Brood-side `(gc-stats)` read before/after a run), not another wall+RSS pass.

### 🥉 Tier 2 — lazy / fused `range` (fixes the memory outlier)

**Evidence:** `reduce` is **both** the slowest gap (207×) **and** the only
benchmark where Brood loses on memory (125 MB vs Elixir 94 MB) — because
`(range 1_000_000)` materialises a full 1 M-element list before the fold.

**Idea:** a lazy range, or a `reduce`/`fold`-over-range that fuses element
generation so nothing intermediate is built. Kills the 125 MB and a large chunk
of the 3.6 s. High value: it's the one case that drags *both* axes.

**Measure:** `--only reduce` (watch RSS — target ≤ ~16 MB like the other loops).

### 🔬 Tier 3 — diagnostics (do this to aim the above)

Build a micro-benchmark that isolates a *single* hot operation in a tight
tail-recursive loop and times it: `(+ a b)`, `(nth v i)`, `(assoc m k v)`,
`(< a b)`, a 1-arg function call. That turns the "likely cause" guesses above
into hard per-op nanosecond costs, so you optimise the op the clock actually
points at. (`(bench "label" expr)` is built in.)

---

## Quick wins worth a look (beat Elixir on short tasks)

These are within ~2× of Elixir's wall — getting Brood compute under ~310 ms
flips them from "loss" to "win" end-to-end:

- ~~**primes**~~ — ✅ **now beats Elixir** (348 ms vs ~368 ms) after update 4.
  *(Note: hoisting a float `√n` bound made it **slower** — mixed int/float
  compare costs more than the int multiply. Kept integer, and that paid off.)*
- **strings (488 ms)** — `(join "," (map number->string (range n)))`; leans on
  `number->string` + list building. ~1.5× off.
- **wordcount (540 ms)** — per-token immutable-map `assoc`; benefits from cheaper
  map update / allocation (Tier 2). ~1.6× off.
- **spawn (634 ms)** — process spawn + message throughput; already only 1.8×.

---

## What NOT to chase

- **Algorithmic cheating** (memoised fib, sieve instead of trial-division, etc.)
  — breaks the cross-language comparison. Keep algorithms + checksums identical.
- **`sort`, startup** — already winning or builtin-bound (Rust); little to gain.
- **Matching Node on raw compute** — a tree-walker won't catch an optimising
  JIT; the realistic bar is **beating Elixir end-to-end** on more rows by
  combining fast startup with a faster eval loop.

---

## Progress log

Record each runtime change here so we can see the trend (best-of-3 wall, ms).

| date | change | loop | collatz | matmul | reduce | fib | notes |
|------|--------|-----:|--------:|-------:|-------:|----:|-------|
| baseline | tree-walker | 3650 | 5900 | 3630 | 4900 | 2400 | initial |
| update 1 | arithmetic/call path | 3290 | 4650 | 3390 | 3830 | 1830 | −15–19% on arith-heavy |
| update 2 | broad runtime | 2940 | 4220 | 3120 | 3580 | 1710 | matmul/bintree moved too |
| update 3 | GC tweaks | 2960 | 4230 | 3120 | 3590 | 1710 | flat (±2%); peak RSS unchanged — see note |
| update 4 | iteration/index path | 2220 | 4250 | 2630 | 3540 | 1710 | loop −25%, matmul −16%; primes now beats Elixir. collatz/fib/reduce flat |
