# Brood — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-22-generic-x86_64-with-glibc2.43 — 2026-06-08 22:41.
> **Runtimes:** Brood brood 0.1.0.

_best of 3 runs per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 28.1ms | 1.0× | 1/1 | 28.1ms | — | 12.3 MB | 1/1 | 0 |

## fib — naive recursion / function-call overhead  (N=30)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 235.3ms | 1.0× | 1/1 | 263.4ms | 28.1ms | 12.4 MB | 1/1 | 832040 |

## loop — raw iteration (tail recursion vs for-loop)  (N=3000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 155.8ms | 1.0× | 1/1 | 183.9ms | 28.1ms | 12.5 MB | 1/1 | 3000000 |

## reduce — higher-order fold over a range  (N=1000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 106.6ms | 1.0× | 1/1 | 134.7ms | 28.1ms | 12.6 MB | 1/1 | 499999500000 |

## primes — integer arithmetic (trial division)  (N=20000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 25.3ms | 1.0× | 1/1 | 53.4ms | 28.1ms | 12.5 MB | 1/1 | 2262 |

## collatz — integer arithmetic + tight inner loop  (N=30000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 294.3ms | 1.0× | 1/1 | 322.4ms | 28.1ms | 21.4 MB | 1/1 | 307 |

## mandelbrot — floating-point math (escape iterations)  (N=128)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 96.3ms | 1.0× | 1/1 | 124.4ms | 28.1ms | 12.4 MB | 1/1 | 345426 |

## matmul — nested loops + indexing (integer NxN)  (N=80)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 798.4ms | 1.0× | 1/1 | 826.5ms | 28.1ms | 23.8 MB | 1/1 | 229499993 |

## strings — string building (join) + length  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 165.8ms | 1.0× | 1/1 | 193.9ms | 28.1ms | 42.4 MB | 1/1 | 288889 |

## wordcount — hash-map build (immutable vs mutable)  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 217.1ms | 1.0× | 1/1 | 245.2ms | 28.1ms | 27.8 MB | 1/1 | 50038280 |

## bintree — allocation / GC pressure (build+walk trees)  (N=40)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 476.9ms | 1.0× | 1/1 | 505.0ms | 28.1ms | 16.7 MB | 1/1 | 327640 |

## sort — sort a list of ints + checksum walk  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 39.9ms | 1.0× | 1/1 | 68.0ms | 28.1ms | 19.3 MB | 1/1 | 102632633 |

## spawn — lightweight concurrent units + result collection  (N=20000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 1.152s | 1.0× | 1/1 | 1.180s | 28.1ms | 164.6 MB | 1/1 | 12200000 |

## pfib — parallel fib — 100 computed at once across cores  (N=28)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 2.400s | 1.0× | 1/1 | 2.428s | 28.1ms | 12.5 MB | 1/1 | 31781100 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 193.3ms | 1.0× | 1/1 | 221.4ms | 28.1ms | 90.6 MB | 1/1 | 500 |
