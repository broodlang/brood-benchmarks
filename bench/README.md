# Cross-language micro-benchmarks: Brood vs Elixir vs Python vs Node

A suite of small programs implemented **four times** — once in each language —
to see where the Brood interpreter is faster or slower than the alternatives.
Each program is named identically across languages (`fib.blsp`, `fib.exs`,
`fib.py`, `fib.js`) so the four implementations sit side by side and can be
diffed directly.

## What's measured

For every (benchmark × language) pair the harness records:

- **Wall time** — total process time, *including* interpreter/VM startup. Best
  of N runs (least-noisy). Measured with `time.perf_counter()` around the child.
- **Peak RSS** — maximum resident memory, from `/usr/bin/time -v`.
- **Checksum** — each program prints one integer. The harness asserts all four
  languages produce the **same** checksum, so we know they did equivalent work.

Because wall time includes startup, the dedicated `startup` benchmark (a bare
"print 0") isolates the fixed cost; compute time for the others is roughly
`wall − startup`.

## The benchmarks (13)

| name | stresses |
|------|----------|
| `startup`    | interpreter/VM startup + base memory |
| `fib`        | naive recursion / function-call overhead (`fib(30)`) |
| `loop`       | raw iteration — tail recursion vs a `for` loop |
| `reduce`     | higher-order fold over a materialised range |
| `primes`     | integer arithmetic — count primes by trial division |
| `collatz`    | integer arithmetic in a tight inner loop |
| `mandelbrot` | floating-point math — escape iterations over a grid |
| `matmul`     | nested loops + indexing — integer N×N multiply |
| `strings`    | string building (`join`) + length |
| `wordcount`  | hash-map build — **immutable** (Brood/Elixir) vs **mutable** (Python/Node) |
| `bintree`    | allocation / GC pressure — build & walk many binary trees |
| `sort`       | sort a list of ints + an order-sensitive checksum walk |
| `spawn`      | lightweight processes + messaging (**Brood & Elixir only**) |

`spawn` has no Python/Node port on purpose: green processes / actors are a
first-class feature of Brood and the BEAM, and OS threads or an event loop
aren't a like-for-like comparison. It's the one benchmark that plays to the
concurrency model rather than raw single-thread speed.

## Fairness notes

- **Same algorithm, same inputs, same output.** Where data is generated
  (`sort`, `wordcount`) every language runs the *identical* LCG
  (`x = (x*1103515245 + 12345) & 0x7fffffff`, seed `123456789`), so all four
  sort/tally the same stream. Checksums confirm it.
  - In **Node** that multiply exceeds the `2^53` safe-integer range, so the LCG
    uses `BigInt` to stay bit-identical to the others.
- **Idiomatic, not adversarial.** Each version is written the way you'd
  naturally write it in that language: tail recursion + immutable maps in
  Brood/Elixir, `for` loops + mutable dicts in Python/Node. That's the point —
  we're comparing the languages as used, not forcing one style on all.
- Float results (`mandelbrot`) rely on IEEE-754 `f64` behaving identically
  across all four runtimes — confirmed by matching checksums.
- Workload sizes are picked so the *slowest* runtime (the Brood bytecode VM)
  finishes in a few seconds; the compiled/JIT runtimes finish in milliseconds.
  That spread is the result, not a problem.

## Running it

```sh
python3 bench/harness.py                      # full suite, best of 3
python3 bench/harness.py --quick              # smaller sizes, smoke test
python3 bench/harness.py --runs 5
python3 bench/harness.py --only fib,sort      # subset
python3 bench/harness.py --langs brood,python # subset of languages
```

Workload sizes are read from `BENCH_N` (the harness sets it); each program has
a sensible default baked in, so you can also run one directly:

```sh
BENCH_N=35 brood bench/brood/fib.blsp
BENCH_N=35 node  bench/node/fib.js
```

Output lands in `results/`: `results.json` (raw numbers) and `report.md`
(formatted tables with each language's time, slowdown vs the fastest, peak RSS,
and checksum).
