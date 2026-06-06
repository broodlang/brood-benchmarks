# What to expect from Brood — benchmark results

Fifteen small programs, each written **six times** — in Brood, Elixir, Python,
Node, Ruby, and **.NET** (C#) — and run under one identical harness. The goal
isn't to crown a winner; it's to give an honest, realistic picture of what you
get with Brood and where it costs you, measured against five well-known runtimes
spanning interpreters (Python, Ruby) and JITs (Node/V8, Elixir/BeamAsm, .NET/RyuJIT).

> Every program prints a checksum, and the harness verifies **all six languages
> produce the same answer** on every benchmark — so this is the same work, six
> ways, not different amounts of it.

> **Engine:** Brood runs on its bytecode VM (the closure-compiling engine that
> replaced the original tree-walker), with **primitive inlining** — the core
> arithmetic/comparison ops (`+ - * < <= =`) execute inline as native `i64`
> operations instead of through a dispatched call. Four runtime changes show up
> below: a **reducible lazy range** so `(range n)` folds without materialising a
> list (`reduce` 1.58 s → 0.27 s, 130 MB → 20 MB); a **process-count-aware GC
> floor** that cut parallel fan-out's peak memory ~35× (`pfib` ~980 MB → ~28 MB);
> **routing spawned processes through the VM** (they were tree-walked even under
> the VM), cutting `pfib`'s *wall time* ~4× (3.84 s → ~1 s); and a **leaner call
> path** (one fewer `Arc` clone per closure call, ~3–4% across call-heavy code).
> The numbers below are that engine.

## The honest summary

- **Memory — Brood's clear strength.** A ~11 MB base, holding 11–38 MB across
  *every* workload (the old 130 MB `reduce` outlier is gone — see the engine
  note), versus Elixir's 90–115 MB, Node's 44–69 MB, and .NET's ~25–47 MB. Only
  Python (~10 MB) is in the same weight class. Startup is ~28 ms: Python edges it,
  Node and .NET tie it (~21–24 ms), Ruby trails (~44 ms), and it's ~12× ahead of
  Elixir's BEAM — so Brood still finishes short tasks before the BEAM has booted.
- **Raw single-threaded compute — Brood's weakest area.** This is where the JITs
  pull away: **.NET (RyuJIT) and Node (V8)** lead, with **Elixir (BeamAsm)** close
  behind once you discount its boot — and even the no-JIT interpreters (Ruby,
  Python) beat Brood. On the per-benchmark wall numbers Brood trails the JITs
  ~15–37×; on *pure compute* (startup excluded — see the chart below) the gap is
  larger still. Brood's young bytecode VM has real headroom here; primitive
  inlining and a leaner call path narrowed it, but compute is where Brood pays.
- **Concurrency depends on the workload.** Cheap, plentiful lightweight processes
  and **concurrent I/O** are genuine strengths: `spawn` **edges out Elixir**
  (327 ms vs 350 ms, at a third of its memory — and the only two with real
  green-process/actor models), and `http` runs in the front group (256 ms, behind
  Node's 209 ms). **Parallel CPU** (`pfib`) is respectable on wall (~1 s, no
  longer the ~4 s / ~980 MB disaster) and the lightest in the field at 27 MB — but
  here .NET is untouchable (**46 ms**: RyuJIT + `Parallel.For`), so Brood is last
  on wall while compute-bound. All below.

---

## Full results — total wall time

The whole process, start to finish (startup + work). 🥇 marks the fastest in
each row. `N` is the workload size.

| benchmark | what it stresses | N | brood | elixir | python | node | ruby | .NET |
|-----------|------------------|--:|------:|-------:|-------:|-----:|-----:|-----:|
| startup | cold start + base memory | — | 28 ms | 345 ms | **11 ms** 🥇 | 21 ms | 44 ms | 24 ms |
| fib | deep recursion | 30 | 497 ms | 373 ms | 73 ms | **31 ms** 🥇 | 101 ms | 31 ms |
| loop | 3 M-iteration count | 3 M | 544 ms | 375 ms | 191 ms | **28 ms** 🥇 | 118 ms | 34 ms |
| reduce | fold over 1 M numbers | 1 M | 272 ms | 350 ms | **19 ms** 🥇 | 30 ms | 42 ms | 25 ms |
| primes | trial-division | 20 k | 96 ms | 372 ms | **22 ms** 🥇 | 31 ms | 54 ms | 30 ms |
| collatz | tight integer loop | 30 k | 881 ms | 372 ms | 238 ms | 32 ms | 136 ms | **28 ms** 🥇 |
| mandelbrot | floating-point | 128 | 385 ms | 419 ms | 77 ms | 28 ms | 71 ms | **27 ms** 🥇 |
| matmul | nested loops + indexing | 80 | 895 ms | 371 ms | 51 ms | 25 ms | 68 ms | **24 ms** 🥇 |
| strings | string building | 50 k | 287 ms | 310 ms | **15 ms** 🥇 | 31 ms | 49 ms | 27 ms |
| wordcount | hash-map build | 100 k | 667 ms | 322 ms | 33 ms | **29 ms** 🥇 | 52 ms | 32 ms |
| bintree | allocation / GC | 40 | 585 ms | 356 ms | 29 ms | **27 ms** 🥇 | 61 ms | 29 ms |
| sort | sort + checksum walk | 50 k | 140 ms | 336 ms | **29 ms** 🥇 | 45 ms | 56 ms | 40 ms |
| spawn | 20 k lightweight processes | 20 k | **327 ms** 🥇 | 350 ms | — | — | — | — |
| pfib | 100 fibs **in parallel** | 28 | 957 ms | 387 ms | 297 ms | 135 ms | 177 ms | **46 ms** 🥇 |
| http | 500 **concurrent** HTTP GETs | 500 | 256 ms | 653 ms | 310 ms | **209 ms** 🥇 | 343 ms | 300 ms |

The story in one line: **the three JITs (Node, .NET, warm Elixir) own raw
compute, .NET most of all** — it wins `collatz`/`mandelbrot`/`matmul` outright
and ties `fib`; **Python is the lightweight-but-quick interpreter**; and **Brood
wins `spawn`, ties for lightest memory, and trails badly on compute.** The
runtime changes that show here: **`reduce` 1.58 s → 0.27 s, 130 MB → 20 MB** (the
reducible lazy range — `(range n)` no longer materialises a million-element list;
the fold streams it); **`pfib` 3.84 s → ~1 s** (spawned bodies now run on the VM,
not the tree-walker) **and ~980 MB → ~28 MB** (a process-count-aware GC floor);
and a **leaner call path** (~3–4% across call-heavy code). (`pfib` is the most
load-sensitive row; it has bounced ~0.8–1.1 s across runs.)

## Where the languages land

Two axes tell most of the story: **compute speed** (geometric aggregate, *startup
excluded* — so the BEAM's slow boot doesn't masquerade as slow compute) against
**memory footprint**. Down-and-left is fast-and-light.

![Where the languages land — compute speed vs memory](results/positioning.svg)

It maps cleanly to what each runtime is: **.NET and Node** in the fast-compute
column (RyuJIT / V8), **Elixir** fast-compute but heavy (the BEAM), **Python**
light and mid-pack, **Ruby** balanced, and **Brood** alone in the *light-but-slow*
corner — the lightest runtime that isn't Python, paying for it in raw compute.
(Startup excluded is deliberate: by wall, Elixir's ~345 ms boot would put it at
the slow end even though its warm compute beats Ruby and Python — see the
`compute` column in [`results/report.md`](results/report.md).)

## The same program, six ways

`fib` — naive recursion, the function-call-overhead benchmark. Each version is
written the way you'd naturally write it in that language; the harness checks
they all print the same number.

```lisp
;; Brood
(defn fib (m) (if (< m 2) m (+ (fib (- m 1)) (fib (- m 2)))))
```
```elixir
# Elixir — multi-clause with a guard
def fib(n) when n < 2, do: n
def fib(n), do: fib(n - 1) + fib(n - 2)
```
```python
# Python
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)
```
```javascript
// Node
function fib(n) { return n < 2 ? n : fib(n - 1) + fib(n - 2); }
```
```ruby
# Ruby
def fib(n) = n < 2 ? n : fib(n - 1) + fib(n - 2)
```
```csharp
// .NET (C#)
static long Fib(int n) => n < 2 ? n : Fib(n - 1) + Fib(n - 2);
```

The concurrency benchmarks are where the *models* diverge most — Brood and Elixir
spawn lightweight green processes; Node uses `worker_threads`; .NET uses
`Parallel.For`; Python and Ruby fork a process pool. All fifteen programs in all
six languages live under [`bench/`](bench/), named identically except the
extension so they diff side by side.

## Biggest gaps — where to focus next

Ranked by how far Brood trails the **fastest other** language (wall) and the
**lightest other** (memory). Worst first — these are the optimization targets;
everything not listed is already within ~2× on at least one axis.

| benchmark | wall gap | mem gap | what it points at |
|-----------|---------:|--------:|-------------------|
| `matmul` | **37×** | 2.0× | nested loops + `vector` indexing — the index path and loop trampoline. |
| `collatz` | 31× | 2.0× | tight integer loop — raw per-iteration VM dispatch overhead. |
| `wordcount` | 23× | 3.1× | immutable hash-map **insert churn** — the persistent-map (HAMT) build/copy cost. |
| `bintree` | 22× | 1.6× | allocation / GC pressure — building and walking many small trees. |
| `loop` / `strings` | ~19× | 1.2–2.9× | per-iteration VM dispatch / string-building churn. |
| `fib` / `reduce` | ~14–16× | 1.2–2.1× | function-call overhead / the fold's per-element apply (no longer a memory outlier). |

The bar is now set by the **JITs** (with .NET in the field it's usually .NET or
Node that's fastest), so the compute gaps look a touch larger than against the
interpreters alone — but the through-line is unchanged: **single-thread compute**
and **immutable-collection churn**, no outlier left. `reduce` used to stand alone
(90× and 130 MB); the reducible range closed it. The concurrency and startup rows
are already ahead or close (`spawn` **0.9× — Brood wins**, `http` 1.2×, `startup`
~2.5×) — `pfib` is the exception only because **.NET is 21× faster there**; against
the rest of the field Brood is ~7× off. Compute is where the distance is.

---

## Memory & startup — where Brood is light

| | cold start | memory at rest |
|---|---:|---:|
| Python | **11 ms** 🥇 | 10 MB |
| Brood | 28 ms | **11 MB** |
| Node | 21 ms | 45 MB |
| .NET | 24 ms | 25 MB |
| Ruby | 44 ms | 23 MB |
| Elixir | 345 ms | 90 MB |

Memory is the durable win: Brood holds **11–38 MB across every workload** — a
fraction of Elixir's 90–115 MB, well under Node's 44–69 MB and .NET's 25–47 MB,
and lighter than Ruby's steady ~23 MB — staying essentially tied with Python for
lightest at rest. Startup is ~28 ms: Python edges it, Node and .NET tie it,
Ruby trails at ~44 ms, but it's still ~12× ahead of Elixir's BEAM, which spends a
third of a second warming up. For short-lived work that's why Brood still beats
Elixir end-to-end on the quick tasks (`primes`, `sort`): the BEAM's compiled code
is fast, but Brood has finished before it's ready.

There used to be one exception — `reduce` at 130 MB, because `(range 1_000_000)`
materialised the whole list where the others stream it. The **reducible lazy
range** (engine note) fixed that: `reduce` now folds the range in a counted loop
with no list at all, at **20 MB** — so there's no longer a single workload where
Brood is the memory outlier.

## Raw compute — Brood's weakest area, and not just versus a JIT

When the work is a tight loop running inside the language, Brood trails everyone.
`matmul` ≈ 0.90 s, `collatz` ≈ 0.88 s, `wordcount` ≈ 0.67 s, `loop` ≈ 0.54 s,
`fib` ≈ 0.50 s. The bar is the two strong **JITs** — **.NET (RyuJIT)** edges
**Node (V8)** for the fastest compute in the suite (`matmul` 24 ms, `collatz`
28 ms), putting Brood **~25–37× behind** on those rows. That much is expected
against native codegen. The telling part is that even the **no-JIT interpreters**
beat Brood: Ruby by **~5–16×** (`fib` 101 ms vs 497 ms, `matmul` 68 ms vs 895 ms),
Python by ~3–7× on the tight loops (and more on allocation-heavy `bintree`/
`wordcount`, where C-backed mutable structures pull ahead). So a chunk of this
isn't the JIT gap — it's headroom left in a young VM. Primitive inlining and a
leaner call path narrowed it, but the compute engine has real distance to make up.

**A fairness note (it surprises people):** by *wall* time Elixir looks slow here,
but that's almost entirely BEAM boot (~345 ms). Subtract each language's startup
and Elixir's *compute* is fast — faster than Ruby and Python on the tight loops
(`collatz` ~24 ms vs Ruby ~90 ms, `fib` ~45 ms vs Ruby ~64 ms), because OTP 29
JITs to native via BeamAsm. The new **`compute` column** in
[`results/report.md`](results/report.md) (wall − startup) and the positioning
chart above both show this — it's why a long-running Elixir *service* feels fast
even though these short-lived runs don't flatter it.

If your hot path is number-crunching, Brood is not the tool yet — or push that
work into a Rust-backed builtin (`sort` is Brood's best compute result, 140 ms,
because the sorting itself isn't interpreted; and `reduce` over a `range` now
folds in a Rust counted loop, 0.27 s instead of 1.6 s).

## Parallel CPU work (`pfib`) — fixed from a disaster to merely last

`pfib` computes `fib(28)` **100 times at once**, each language using its
idiomatic parallelism (Brood/Elixir spawn lightweight processes; Node uses
`worker_threads`; .NET uses `Parallel.For`; Python and Ruby fork a process pool).

| lang | wall | peak RSS |
|---|---:|---:|
| .NET | **46 ms** 🥇 | 28 MB |
| node | 135 ms | 343 MB |
| ruby | 177 ms | **24 MB** 🥇 |
| python | 297 ms | 22 MB |
| elixir | 387 ms | 96 MB |
| brood | 957 ms | 27 MB |

.NET is in a class of its own here — RyuJIT makes each `fib(28)` ~30× cheaper
than Brood's interpreter, and `Parallel.For` spreads them across the cores, so it
finishes in 46 ms. This row used to be Brood's worst result by far — **3.84 s and
~980 MB**. Two runtime fixes turned it around:

- **Wall time (3.84 s → ~1 s).** A spawned process's body was running on the
  **tree-walker even under `BROOD_VM=1`** — the `spawn` entry point called the
  tree-walk `apply`, not the VM — so every green process computed ~4–5× slower
  than the identical code at top level. Routing spawned bodies through the VM
  (with its inlined primitives) closed that gap; a single spawned `fib(28)` went
  from 0.66 s to 0.15 s, matching the root thread.
- **Memory (~980 MB → ~28 MB).** Each share-nothing process climbed to its
  single-process GC floor (~64K objects) before its first collection; a
  **process-count-aware GC floor** now divides that budget across the live
  processes, so a wide fan-out collects earlier. Brood is now the **lightest in
  the field at 27 MB** — far under Node (343 MB) and Elixir (96 MB), even edging
  Python and Ruby.

What's left is honest: Brood is **last on wall time** — ~7× off the Node/Ruby/
Python pack and ~21× off .NET — but it's a *compute* gap, not a scheduler one
(the scheduler matches raw OS-process parallelism; the cores, not Brood, set the
ceiling — see the README's note on the asymmetric P/E-core CPU). The fix is
faster per-task compute, the same lever as the `fib` row. (This row saturates
every core, so it's the most load-sensitive in the suite — it has bounced between
~0.8 s and ~1.1 s across runs.)

## Concurrent I/O (`http`) — Brood runs with the front-runners

`http` fires **500 concurrent GETs** at a local server that sleeps 20 ms per
request, so it measures how well each runtime overlaps in-flight requests — pure
I/O concurrency, where raw compute speed barely matters.

| lang | wall | peak RSS |
|---|---:|---:|
| node | **209 ms** 🥇 | 69 MB |
| brood | 256 ms | 85 MB |
| .NET | 300 ms | **46 MB** 🥇 |
| python | 310 ms | 47 MB |
| ruby | 343 ms | 50 MB |
| elixir | 653 ms | 724 MB |

This is the mirror image of `pfib` — the JIT compute advantage barely matters when
the work is *waiting*. Brood's green processes **park** on the response (its TCP
is message-based), so all 500 requests are genuinely in flight at once — and it
lands **2nd, ~22% behind Node** (256 ms vs 209 ms), ahead of .NET's async
`HttpClient`, Python's thread pool, and Ruby. The one cost is memory: with
`net/http` from the brood-net package, peak RSS is ~85 MB here — heavier than
.NET/Python/Ruby (~46–50 MB), though still a fraction of Elixir's 724 MB (its
*stdlib* `:httpc` is slow and heavy; real Elixir services use a client like
Finch). When your work is waiting on I/O, Brood's concurrency model pays off.
(Latency-sensitive; numbers bounce a bit run-to-run, the ordering is stable.)

## Lightweight processes (`spawn`)

Fanning out 20,000 processes that each send one message: Brood **edges out Elixir
end-to-end** (327 ms vs 350 ms) *and* does it in **37 MB vs Elixir's 111 MB**.
These two are the only entrants with a real green-process / actor model (Node,
.NET, Python and Ruby have no like-for-like, so they sit this one out). Cheap,
plentiful processes are a real part of the runtime — note how different this is
from `pfib`: 20,000 *tiny* processes are cheap; 100 *compute-heavy* ones are not.

---

## So when should I use Brood?

**A good fit:**

- Command-line tools and short-lived scripts — fast start, tiny footprint.
- Memory-constrained environments — a fraction of the BEAM's or Node's RAM.
- I/O-bound concurrency — many simultaneous requests/connections, where it's
  competitive with Node (2nd on `http`) and far lighter than stdlib Elixir.

**A poor fit:**

- CPU-bound number crunching — the VM trails the JITs (.NET, Node) heavily and
  the interpreters (Ruby ~5–16×, Python ~3–7×) too. Parallel fan-out is no longer
  a disaster (~1 s, not ~4 s, and the lightest in the field), but per-task compute
  is the bottleneck — and .NET shows the ceiling at 46 ms. Lean on Brood for *I/O*
  concurrency, not *compute* fan-out.
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

_Measured on: Intel Core i7-14700HX (20 cores / 28 threads — 8 P-cores + 12
E-cores) · 61 GB RAM · Ubuntu 26.04 · Brood 0.1.0 (bytecode VM + primitive
inlining + reducible lazy range + process-count-aware GC floor + VM-routed
spawned processes + leaner call path) · Elixir 1.20.0 / OTP 29 (BeamAsm JIT) ·
Python 3.14.4 · Node 24.15.0 (V8) · Ruby 3.3.8 · .NET 10.0.108 (RyuJIT), each
benchmark precompiled (Release) and run as a native binary. Compute rows are
best-of-3 from the full suite; the latency-sensitive `startup` and `http` rows
are best-of-5 measured in isolation so neighbouring benchmarks' load doesn't
inflate them. `pfib` saturates every core and remains the most load-sensitive row
in the suite._
