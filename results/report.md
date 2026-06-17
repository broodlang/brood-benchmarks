# Brood vs Elixir vs Erlang — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-22-generic-x86_64-with-glibc2.43 — 2026-06-17 09:57.
> **Runtimes:** Brood brood 0.1.0; Elixir Elixir 1.20.0 (compiled with Erlang/OTP 28); Erlang Erlang/OTP 28 [BEAM].
> **Isolation:** taskset pin (compute→core 11, concurrency→0-11); 0.25s settle.

_best of 5 runs; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 34.9ms | 1.0× | 1/3 | 34.9ms | — | 21.3 MB | 1/3 | 0 |
| elixir | 193.2ms | 5.5× | 2/3 | 193.2ms | — | 70.4 MB | 2/3 | 0 |
| erlang | 208.7ms | 6.0× | 3/3 | 208.7ms | — | 71.0 MB | 3/3 | 0 |

## fib — naive recursion / function-call overhead  (N=35)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 505.8ms | 6.8× | 3/3 | 540.7ms | 34.9ms | 24.6 MB | 1/3 | 9227465 |
| elixir | 80.4ms | 1.1× | 2/3 | 273.6ms | 193.2ms | 69.8 MB | 2/3 | 9227465 |
| erlang | 74.6ms | 1.0× | 1/3 | 283.3ms | 208.7ms | 71.1 MB | 3/3 | 9227465 |

## loop — raw iteration (tail recursion vs for-loop)  (N=30000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 117.3ms | 2.5× | 3/3 | 152.2ms | 34.9ms | 24.6 MB | 1/3 | 449999985000000 |
| elixir | 77.7ms | 1.7× | 2/3 | 270.9ms | 193.2ms | 69.7 MB | 2/3 | 449999985000000 |
| erlang | 46.8ms | 1.0× | 1/3 | 255.5ms | 208.7ms | 71.2 MB | 3/3 | 449999985000000 |

## reduce — higher-order fold over a range  (N=5000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 119.2ms | 3.0× | 2/3 | 154.1ms | 34.9ms | 21.4 MB | 1/3 | 12499997500000 |
| elixir | 39.2ms | 1.0× | 1/3 | 232.4ms | 193.2ms | 69.7 MB | 2/3 | 12499997500000 |
| erlang | 227.9ms | 5.8× | 3/3 | 436.6ms | 208.7ms | 375.9 MB | 3/3 | 12499997500000 |

## primes — integer arithmetic (trial division)  (N=150000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 41.7ms | 2.5× | 3/3 | 76.6ms | 34.9ms | 24.7 MB | 1/3 | 13848 |
| elixir | 29.8ms | 1.8× | 2/3 | 223.0ms | 193.2ms | 72.1 MB | 2/3 | 13848 |
| erlang | 16.6ms | 1.0× | 1/3 | 225.3ms | 208.7ms | 79.4 MB | 3/3 | 13848 |

## collatz — integer arithmetic + tight inner loop  (N=250000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 502.7ms | 5.0× | 3/3 | 537.6ms | 34.9ms | 38.0 MB | 1/3 | 442 |
| elixir | 103.8ms | 1.0× | 2/3 | 297.0ms | 193.2ms | 70.6 MB | 2/3 | 442 |
| erlang | 100.0ms | 1.0× | 1/3 | 308.7ms | 208.7ms | 79.1 MB | 3/3 | 442 |

## mandelbrot — floating-point math (escape iterations)  (N=540)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 227.4ms | 2.0× | 2/3 | 262.3ms | 34.9ms | 24.8 MB | 1/3 | 6129302 |
| elixir | 257.0ms | 2.3× | 3/3 | 450.2ms | 193.2ms | 70.0 MB | 2/3 | 6129302 |
| erlang | 112.3ms | 1.0× | 1/3 | 321.0ms | 208.7ms | 71.5 MB | 3/3 | 6129302 |

## matmul — nested loops + indexing (integer NxN)  (N=175)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 167.0ms | 2.8× | 3/3 | 201.9ms | 34.9ms | 36.7 MB | 1/3 | 654353666 |
| elixir | 58.9ms | 1.0× | 1/3 | 252.1ms | 193.2ms | 75.9 MB | 3/3 | 654353666 |
| erlang | 79.3ms | 1.3× | 2/3 | 288.0ms | 208.7ms | 74.9 MB | 2/3 | 654353666 |

## strings — string building (join) + length  (N=500000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 12.1ms | 1.0× | 1/3 | 47.0ms | 34.9ms | 31.6 MB | 1/3 | 3388889 |
| elixir | 123.5ms | 10.2× | 3/3 | 316.7ms | 193.2ms | 199.1 MB | 2/3 | 3388889 |
| erlang | 112.8ms | 9.3× | 2/3 | 321.5ms | 208.7ms | 206.9 MB | 3/3 | 3388889 |

## wordcount — hash-map build (immutable vs mutable)  (N=750000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 884.7ms | 7.9× | 3/3 | 919.6ms | 34.9ms | 90.7 MB | 3/3 | 374854840 |
| elixir | 175.7ms | 1.6× | 2/3 | 368.9ms | 193.2ms | 70.8 MB | 1/3 | 374854840 |
| erlang | 112.3ms | 1.0× | 1/3 | 321.0ms | 208.7ms | 73.2 MB | 2/3 | 374854840 |

## bintree — allocation / GC pressure (build+walk trees)  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 414.6ms | 53.2× | 3/3 | 449.5ms | 34.9ms | 35.6 MB | 1/3 | 1638200 |
| elixir | 7.8ms | 1.0× | 1/3 | 201.0ms | 193.2ms | 70.4 MB | 2/3 | 1638200 |
| erlang | 13.9ms | 1.8× | 2/3 | 222.6ms | 208.7ms | 71.6 MB | 3/3 | 1638200 |

## sort — sort a list of ints + checksum walk  (N=375000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 302.7ms | 3.2× | 3/3 | 337.6ms | 34.9ms | 120.4 MB | 1/3 | 46468819 |
| elixir | 120.3ms | 1.3× | 2/3 | 313.5ms | 193.2ms | 156.9 MB | 3/3 | 46468819 |
| erlang | 94.7ms | 1.0× | 1/3 | 303.4ms | 208.7ms | 137.6 MB | 2/3 | 46468819 |

## nqueens — backtracking recursion — count N-queens solutions  (N=10)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 577.2ms | 53.9× | 3/3 | 612.1ms | 34.9ms | 32.6 MB | 1/3 | 724 |
| elixir | 19.3ms | 1.8× | 2/3 | 212.5ms | 193.2ms | 69.6 MB | 2/3 | 724 |
| erlang | 10.7ms | 1.0× | 1/3 | 219.4ms | 208.7ms | 71.7 MB | 3/3 | 724 |

## errors — error handling — raise + recover a value N times  (N=200000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 193.0ms | 29.2× | 3/3 | 227.9ms | 34.9ms | 38.2 MB | 1/3 | 9900000 |
| elixir | 24.2ms | 3.7× | 2/3 | 217.4ms | 193.2ms | 70.6 MB | 2/3 | 9900000 |
| erlang | 6.6ms | 1.0× | 1/3 | 215.3ms | 208.7ms | 82.9 MB | 3/3 | 9900000 |

## errors-deep — error propagation — throw 50 frames deep, catch at top  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 272.8ms | 209.8× | 3/3 | 307.7ms | 34.9ms | 39.3 MB | 1/3 | 2475000 |
| elixir | 20.2ms | 15.5× | 2/3 | 213.4ms | 193.2ms | 69.9 MB | 2/3 | 2475000 |
| erlang | 1.3ms | 1.0× | 1/3 | 210.0ms | 208.7ms | 73.0 MB | 3/3 | 2475000 |

## pipeline — filter/map/reduce pipeline over a range  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 50.4ms | 50.4× | 3/3 | 85.3ms | 34.9ms | 24.8 MB | 1/3 | 155553889038886 |
| elixir | 3.1ms | 3.1× | 2/3 | 196.3ms | 193.2ms | 70.3 MB | 2/3 | 155553889038886 |
| erlang | 0.0ms | < 1× | 1/3 | 201.5ms | 208.7ms | 71.2 MB | 3/3 | 155553889038886 |

## spawn — lightweight concurrent units + result collection  (N=10000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 97.2ms | 8.8× | 3/3 | 132.1ms | 34.9ms | 75.3 MB | 1/3 | 6100000 |
| elixir | 11.1ms | 1.0× | 1/3 | 204.3ms | 193.2ms | 76.3 MB | 2/3 | 6100000 |
| erlang | 14.2ms | 1.3× | 2/3 | 222.9ms | 208.7ms | 79.3 MB | 3/3 | 6100000 |

## pfib — parallel fib — 100 computed at once across cores  (N=28)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 344.9ms | 5.9× | 3/3 | 379.8ms | 34.9ms | 26.6 MB | 1/3 | 31781100 |
| elixir | 96.4ms | 1.6× | 2/3 | 289.6ms | 193.2ms | 71.9 MB | 3/3 | 31781100 |
| erlang | 58.7ms | 1.0× | 1/3 | 267.4ms | 208.7ms | 71.2 MB | 2/3 | 31781100 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 155.6ms | 1.0× | 1/3 | 190.5ms | 34.9ms | 122.6 MB | 1/3 | 500 |
| elixir | 625.9ms | 4.0× | 2/3 | 819.1ms | 193.2ms | 580.4 MB | 3/3 | 500 |
| erlang | 645.7ms | 4.1× | 3/3 | 854.4ms | 208.7ms | 557.6 MB | 2/3 | 500 |
