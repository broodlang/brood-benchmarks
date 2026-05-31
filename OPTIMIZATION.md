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
| sort | 124 ms | 115 ms | 19 MB | 4× | ✅ win |
| primes | 162 ms | 153 ms | 9 MB | 8× | ✅ win |
| strings | 251 ms | 242 ms | 33 MB | 15× | ✅ win |
| mandelbrot | 439 ms | 430 ms | 9 MB | 18× | 1.1× |
| wordcount | 557 ms | 548 ms | 27 MB | 20× | 1.5× |
| spawn | 622 ms | 613 ms | 32 MB | 2× | 1.7× |
| bintree | 691 ms | 682 ms | 21 MB | 26× | 1.8× |
| fib | 828 ms | 819 ms | 9 MB | 25× | 2.3× |
| loop | 1.05 s | 1042 ms | 9 MB | 41× | 3.0× |
| matmul | 1.18 s | 1174 ms | 18 MB | 49× | 3.6× |
| reduce | 1.78 s | 1766 ms | 139 MB ⚠️ | 92× | 5.9× |
| collatz | 2.00 s | 1995 ms | 17 MB | 64× | 5.4× |

**Scorecard vs the worst competitor (always Elixir): wall 4/13 · memory 12/13.**
Memory is already a strength (5–11× lighter than Elixir nearly everywhere); the
work is on **wall time of hot loops in the VM**, plus the **one memory
outlier** (`reduce`, 139 MB). The bytecode VM (ADR-076) roughly halved every
compute row vs the old tree-walker — `strings` now joins `startup`/`primes`/`sort`
in beating Elixir end-to-end, and `mandelbrot` is within 1.1×.

---

## Targets, in priority order

### 🥇 Tier 1 — highest leverage: eval-loop dispatch cost

**Evidence:** `loop` (41×), `collatz` (64×), `fib` (25×) are dominated by raw
per-operation VM dispatch overhead — `loop` does nothing but `(+ i 1)` /
`(>= i n)` and still costs 1.05 s for 3 M iterations (~0.35 µs/iter).

**Why it matters most:** every benchmark pays this tax, so cutting per-op
dispatch cost moves the *whole* table at once. The bytecode VM cutover (ADR-076)
already roughly halved this row — this is the seam that's paying off.

**Ideas to try:** tighter opcode/closure dispatch in the eval loop; avoid
re-resolving global symbols (`+`, `>=`) per call (cache the resolved fn on the
call site); specialise the 2-arg arithmetic/comparison path so variadic `+`/`<`
don't walk an argument list for the common binary case.

**Measure:** `--only loop,collatz,fib` and a Tier-3 micro-benchmark (below).

### 🥈 Tier 2 — collection access: `nth` on vectors

**Evidence:** `matmul` (49×) is `(nth (nth b k) j)` in its inner loop —
two indexes per multiply-add, 80³ = 512 k times.

**Check first:** confirm `nth` on a vector is genuinely O(1) and cheap, not a
bounds-check + generic-seq dispatch per call. If it's slow, a fast vector-index
path helps `matmul` and any indexed workload.

**Measure:** `--only matmul`; micro-bench a tight `(nth v i)` loop.

### 🥈 Tier 2 — allocation / GC: persistent vectors

**Evidence:** `bintree` (26×) builds and walks many small `[l r]` vectors;
`reduce`'s 139 MB is allocation too.

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

**Evidence:** `reduce` is **both** the worst gap (92×) **and** the only
benchmark where Brood loses on memory (139 MB vs Elixir 93 MB) — because
`(range 1_000_000)` materialises a full 1 M-element list before the fold.

**Idea:** a lazy range, or a `reduce`/`fold`-over-range that fuses element
generation so nothing intermediate is built. Kills the 139 MB and a large chunk
of the 1.8 s. High value: it's the one case that drags *both* axes.

**Measure:** `--only reduce` (watch RSS — target ≤ ~16 MB like the other loops).

### 🔬 Tier 3 — diagnostics (do this to aim the above)

Build a micro-benchmark that isolates a *single* hot operation in a tight
tail-recursive loop and times it: `(+ a b)`, `(nth v i)`, `(assoc m k v)`,
`(< a b)`, a 1-arg function call. That turns the "likely cause" guesses above
into hard per-op nanosecond costs, so you optimise the op the clock actually
points at. (`(bench "label" expr)` is built in.)

---

## Quick wins worth a look (beat Elixir on short tasks)

These are within ~2× of Elixir's wall — getting Brood compute under ~300 ms
flips them from "loss" to "win" end-to-end:

- ~~**primes**~~ — ✅ **now beats Elixir** (162 ms vs ~347 ms).
  *(Note: hoisting a float `√n` bound made it **slower** — mixed int/float
  compare costs more than the int multiply. Kept integer, and that paid off.)*
- ~~**strings**~~ — ✅ **now beats Elixir** (251 ms vs ~375 ms) after the VM
  cutover; `(join "," (map number->string (range n)))` leans on `number->string`
  + list building.
- **mandelbrot (439 ms)** — f64 escape loop; the VM brought it to within **1.1×**
  of Elixir — the next row likely to flip.
- **wordcount (557 ms)** — per-token immutable-map `assoc`; benefits from cheaper
  map update / allocation (Tier 2). ~1.5× off.
- **spawn (622 ms)** — process spawn + message throughput; already only 1.7×.

---

## What NOT to chase

- **Algorithmic cheating** (memoised fib, sieve instead of trial-division, etc.)
  — breaks the cross-language comparison. Keep algorithms + checksums identical.
- **`sort`, startup** — already winning or builtin-bound (Rust); little to gain.
- **Matching Node on raw compute** — even a bytecode VM won't catch an
  optimising JIT; the realistic bar is **beating Elixir end-to-end** on more rows
  by combining fast startup with a faster eval loop.

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
| update 5 | bytecode VM (ADR-076) | 1051 | 2004 | 1183 | 1775 | 828 | **VM is now the default engine** — ~2× across the board (collatz −53%, loop −53%, matmul −55%, reduce −50%, fib −52%). strings now beats Elixir; mandelbrot within 1.1× |
