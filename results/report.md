# Brood — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-22-generic-x86_64-with-glibc2.43 — 2026-06-20 17:29.
> **Runtimes:** Brood brood 0.1.0.
> **Isolation:** taskset pin (compute→core 11, concurrency→0-11); 0.25s settle.

_best of 3 runs; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 26.2ms | 1.0× | 1/1 | 26.2ms | — | 18.1 MB | 1/1 | 0 |

## fib — naive recursion / function-call overhead  (N=35)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 233.3ms | 1.0× | 1/1 | 259.5ms | 26.2ms | 21.8 MB | 1/1 | 9227465 |

## loop — raw iteration (tail recursion vs for-loop)  (N=30000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 41.9ms | 1.0× | 1/1 | 68.1ms | 26.2ms | 21.6 MB | 1/1 | 449999985000000 |

## reduce — higher-order fold over a range  (N=5000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 3.2ms | 1.0× | 1/1 | 29.4ms | 26.2ms | 18.3 MB | 1/1 | 12499997500000 |

## primes — integer arithmetic (trial division)  (N=150000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 41.3ms | 1.0× | 1/1 | 67.5ms | 26.2ms | 21.6 MB | 1/1 | 13848 |

## collatz — integer arithmetic + tight inner loop  (N=250000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 89.4ms | 1.0× | 1/1 | 115.6ms | 26.2ms | 21.6 MB | 1/1 | 442 |

## mandelbrot — floating-point math (escape iterations)  (N=540)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 241.6ms | 1.0× | 1/1 | 267.8ms | 26.2ms | 21.6 MB | 1/1 | 6129302 |

## matmul — nested loops + indexing (integer NxN)  (N=175)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 101.3ms | 1.0× | 1/1 | 127.5ms | 26.2ms | 34.3 MB | 1/1 | 654353666 |

## strings — string building (join) + length  (N=500000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 12.9ms | 1.0× | 1/1 | 39.1ms | 26.2ms | 28.5 MB | 1/1 | 3388889 |

## wordcount — hash-map build (immutable vs mutable)  (N=750000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 399.9ms | 1.0× | 1/1 | 426.1ms | 26.2ms | 90.4 MB | 1/1 | 374854840 |

## bintree — allocation / GC pressure (build+walk trees)  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 105.5ms | 1.0× | 1/1 | 131.7ms | 26.2ms | 36.8 MB | 1/1 | 1638200 |

## sort — sort a list of ints + checksum walk  (N=375000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 181.8ms | 1.0× | 1/1 | 208.0ms | 26.2ms | 129.8 MB | 1/1 | 46468819 |

## nqueens — backtracking recursion — count N-queens solutions  (N=10)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 110.3ms | 1.0× | 1/1 | 136.5ms | 26.2ms | 31.5 MB | 1/1 | 724 |

## errors — error handling — raise + recover a value N times  (N=200000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 191.1ms | 1.0× | 1/1 | 217.3ms | 26.2ms | 33.7 MB | 1/1 | 9900000 |

## errors-deep — error propagation — throw 50 frames deep, catch at top  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 307.9ms | 1.0× | 1/1 | 334.1ms | 26.2ms | 34.1 MB | 1/1 | 2475000 |

## pipeline — filter/map/reduce pipeline over a range  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 37.2ms | 1.0× | 1/1 | 63.4ms | 26.2ms | 21.6 MB | 1/1 | 155553889038886 |

## spawn — lightweight concurrent units + result collection  (N=10000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 103.8ms | 1.0× | 1/1 | 130.0ms | 26.2ms | 74.2 MB | 1/1 | 6100000 |

## pfib — parallel fib — 100 computed at once across cores  (N=28)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 358.3ms | 1.0× | 1/1 | 384.5ms | 26.2ms | 25.8 MB | 1/1 | 31781100 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 149.6ms | 1.0× | 1/1 | 175.8ms | 26.2ms | 114.6 MB | 1/1 | 500 |
