# Brood vs Elixir — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-22-generic-x86_64-with-glibc2.43 — 2026-06-21 09:19.
> **Runtimes:** Brood brood 0.1.0; Elixir Elixir 1.20.0 (compiled with Erlang/OTP 28).
> **Isolation:** taskset pin (compute→core 11, concurrency→0-11); 0.25s settle.

_best of 3 runs; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 26.2ms | 1.0× | 1/2 | 26.2ms | — | 18.3 MB | 1/2 | 0 |
| elixir | 202.7ms | 7.7× | 2/2 | 202.7ms | — | 69.7 MB | 2/2 | 0 |

## fib — naive recursion / function-call overhead  (N=35)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 223.0ms | 3.0× | 2/2 | 249.2ms | 26.2ms | 22.0 MB | 1/2 | 9227465 |
| elixir | 75.4ms | 1.0× | 1/2 | 278.1ms | 202.7ms | 69.7 MB | 2/2 | 9227465 |

## loop — raw iteration (tail recursion vs for-loop)  (N=30000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 37.5ms | 1.0× | 1/2 | 63.7ms | 26.2ms | 21.7 MB | 1/2 | 449999985000000 |
| elixir | 60.3ms | 1.6× | 2/2 | 263.0ms | 202.7ms | 69.9 MB | 2/2 | 449999985000000 |

## reduce — higher-order fold over a range  (N=5000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 3.4ms | 1.0× | 1/2 | 29.6ms | 26.2ms | 18.3 MB | 1/2 | 12499997500000 |
| elixir | 31.2ms | 9.2× | 2/2 | 233.9ms | 202.7ms | 69.8 MB | 2/2 | 12499997500000 |

## primes — integer arithmetic (trial division)  (N=150000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 38.9ms | 2.9× | 2/2 | 65.1ms | 26.2ms | 21.8 MB | 1/2 | 13848 |
| elixir | 13.4ms | 1.0× | 1/2 | 216.1ms | 202.7ms | 69.8 MB | 2/2 | 13848 |

## collatz — integer arithmetic + tight inner loop  (N=250000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 82.4ms | 1.0× | 1/2 | 108.6ms | 26.2ms | 21.7 MB | 1/2 | 442 |
| elixir | 106.2ms | 1.3× | 2/2 | 308.9ms | 202.7ms | 69.7 MB | 2/2 | 442 |

## mandelbrot — floating-point math (escape iterations)  (N=540)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 225.2ms | 1.0× | 1/2 | 251.4ms | 26.2ms | 21.7 MB | 1/2 | 6129302 |
| elixir | 254.8ms | 1.1× | 2/2 | 457.5ms | 202.7ms | 70.1 MB | 2/2 | 6129302 |

## matmul — nested loops + indexing (integer NxN)  (N=175)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 102.4ms | 1.8× | 2/2 | 128.6ms | 26.2ms | 39.4 MB | 1/2 | 654353666 |
| elixir | 58.4ms | 1.0× | 1/2 | 261.1ms | 202.7ms | 75.4 MB | 2/2 | 654353666 |

## strings — string building (join) + length  (N=500000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 12.2ms | 1.0× | 1/2 | 38.4ms | 26.2ms | 28.3 MB | 1/2 | 3388889 |
| elixir | 114.9ms | 9.4× | 2/2 | 317.6ms | 202.7ms | 199.2 MB | 2/2 | 3388889 |

## wordcount — hash-map build (immutable vs mutable)  (N=750000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 395.2ms | 2.3× | 2/2 | 421.4ms | 26.2ms | 90.3 MB | 2/2 | 374854840 |
| elixir | 171.9ms | 1.0× | 1/2 | 374.6ms | 202.7ms | 70.7 MB | 1/2 | 374854840 |

## bintree — allocation / GC pressure (build+walk trees)  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 102.6ms | 6.5× | 2/2 | 128.8ms | 26.2ms | 36.0 MB | 1/2 | 1638200 |
| elixir | 15.8ms | 1.0× | 1/2 | 218.5ms | 202.7ms | 70.1 MB | 2/2 | 1638200 |

## sort — sort a list of ints + checksum walk  (N=375000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 172.4ms | 1.5× | 2/2 | 198.6ms | 26.2ms | 129.8 MB | 1/2 | 46468819 |
| elixir | 112.4ms | 1.0× | 1/2 | 315.1ms | 202.7ms | 156.8 MB | 2/2 | 46468819 |

## nqueens — backtracking recursion — count N-queens solutions  (N=10)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 115.3ms | 17.5× | 2/2 | 141.5ms | 26.2ms | 33.2 MB | 1/2 | 724 |
| elixir | 6.6ms | 1.0× | 1/2 | 209.3ms | 202.7ms | 69.7 MB | 2/2 | 724 |

## errors — error handling — raise + recover a value N times  (N=200000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 40.7ms | 2.2× | 2/2 | 66.9ms | 26.2ms | 19.3 MB | 1/2 | 9900000 |
| elixir | 18.1ms | 1.0× | 1/2 | 220.8ms | 202.7ms | 69.9 MB | 2/2 | 9900000 |

## errors-deep — error propagation — throw 50 frames deep, catch at top  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 107.6ms | 14.5× | 2/2 | 133.8ms | 26.2ms | 21.6 MB | 1/2 | 2475000 |
| elixir | 7.4ms | 1.0× | 1/2 | 210.1ms | 202.7ms | 69.8 MB | 2/2 | 2475000 |

## pipeline — filter/map/reduce pipeline over a range  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 38.1ms | 5.4× | 2/2 | 64.3ms | 26.2ms | 21.6 MB | 1/2 | 155553889038886 |
| elixir | 7.1ms | 1.0× | 1/2 | 209.8ms | 202.7ms | 70.5 MB | 2/2 | 155553889038886 |

## spawn — lightweight concurrent units + result collection  (N=10000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 119.7ms | 12.9× | 2/2 | 145.9ms | 26.2ms | 72.7 MB | 1/2 | 6100000 |
| elixir | 9.3ms | 1.0× | 1/2 | 212.0ms | 202.7ms | 76.2 MB | 2/2 | 6100000 |

## pfib — parallel fib — 100 computed at once across cores  (N=28)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 377.3ms | 5.4× | 2/2 | 403.5ms | 26.2ms | 26.6 MB | 1/2 | 31781100 |
| elixir | 70.0ms | 1.0× | 1/2 | 272.7ms | 202.7ms | 72.4 MB | 2/2 | 31781100 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 151.6ms | 1.0× | 1/2 | 177.8ms | 26.2ms | 114.8 MB | 1/2 | 500 |
| elixir | 583.5ms | 3.8× | 2/2 | 786.2ms | 202.7ms | 493.1 MB | 2/2 | 500 |
