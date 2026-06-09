# Brood vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-22-generic-x86_64-with-glibc2.43 — 2026-06-09 20:38.
> **Runtimes:** Brood brood 0.1.0; Elixir Elixir 1.20.0 (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.108.

_best of 3 runs per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 28.2ms | 2.7× | 4/6 | 28.2ms | — | 14.3 MB | 2/6 | 0 |
| elixir | 258.9ms | 24.9× | 6/6 | 258.9ms | — | 76.4 MB | 6/6 | 0 |
| python | 10.4ms | 1.0× | 1/6 | 10.4ms | — | 9.7 MB | 1/6 | 0 |
| node | 18.3ms | 1.8× | 2/6 | 18.3ms | — | 43.3 MB | 5/6 | 0 |
| ruby | 44.0ms | 4.2× | 5/6 | 44.0ms | — | 23.5 MB | 3/6 | 0 |
| dotnet | 22.1ms | 2.1× | 3/6 | 22.1ms | — | 25.7 MB | 4/6 | 0 |

## fib — naive recursion / function-call overhead  (N=30)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 226.1ms | 68.5× | 6/6 | 254.3ms | 28.2ms | 14.2 MB | 2/6 | 832040 |
| elixir | 53.7ms | 16.3× | 3/6 | 312.6ms | 258.9ms | 80.7 MB | 6/6 | 832040 |
| python | 66.3ms | 20.1× | 4/6 | 76.7ms | 10.4ms | 9.8 MB | 1/6 | 832040 |
| node | 7.2ms | 2.2× | 2/6 | 25.5ms | 18.3ms | 48.5 MB | 5/6 | 832040 |
| ruby | 67.9ms | 20.6× | 5/6 | 111.9ms | 44.0ms | 23.5 MB | 3/6 | 832040 |
| dotnet | 3.3ms | 1.0× | 1/6 | 25.4ms | 22.1ms | 25.7 MB | 4/6 | 832040 |

## loop — raw iteration (tail recursion vs for-loop)  (N=3000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 155.1ms | 110.8× | 5/6 | 183.3ms | 28.2ms | 14.2 MB | 2/6 | 3000000 |
| elixir | 42.8ms | 30.6× | 3/6 | 301.7ms | 258.9ms | 80.9 MB | 6/6 | 3000000 |
| python | 194.6ms | 139.0× | 6/6 | 205.0ms | 10.4ms | 9.8 MB | 1/6 | 3000000 |
| node | 2.5ms | 1.8× | 2/6 | 20.8ms | 18.3ms | 48.3 MB | 5/6 | 3000000 |
| ruby | 60.9ms | 43.5× | 4/6 | 104.9ms | 44.0ms | 23.5 MB | 3/6 | 3000000 |
| dotnet | 1.4ms | 1.0× | 1/6 | 23.5ms | 22.1ms | 26.1 MB | 4/6 | 3000000 |

## reduce — higher-order fold over a range  (N=1000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 95.2ms | 95.2× | 6/6 | 123.4ms | 28.2ms | 14.1 MB | 2/6 | 499999500000 |
| elixir | 8.4ms | 8.4× | 5/6 | 267.3ms | 258.9ms | 78.3 MB | 6/6 | 499999500000 |
| python | 6.3ms | 6.3× | 4/6 | 16.7ms | 10.4ms | 9.8 MB | 1/6 | 499999500000 |
| node | 2.2ms | 2.2× | 3/6 | 20.5ms | 18.3ms | 50.2 MB | 5/6 | 499999500000 |
| ruby | 0.0ms | < 1× | 1/6 | 40.6ms | 44.0ms | 23.5 MB | 3/6 | 499999500000 |
| dotnet | 0.9ms | < 1× | 2/6 | 23.0ms | 22.1ms | 26.2 MB | 4/6 | 499999500000 |

## primes — integer arithmetic (trial division)  (N=20000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 23.6ms | 23.6× | 5/6 | 51.8ms | 28.2ms | 14.1 MB | 2/6 | 2262 |
| elixir | 49.0ms | 49.0× | 6/6 | 307.9ms | 258.9ms | 81.6 MB | 6/6 | 2262 |
| python | 7.9ms | 7.9× | 4/6 | 18.3ms | 10.4ms | 9.9 MB | 1/6 | 2262 |
| node | 0.7ms | < 1× | 1/6 | 19.0ms | 18.3ms | 49.0 MB | 5/6 | 2262 |
| ruby | 6.7ms | 6.7× | 3/6 | 50.7ms | 44.0ms | 23.5 MB | 3/6 | 2262 |
| dotnet | 1.5ms | 1.5× | 2/6 | 23.6ms | 22.1ms | 26.1 MB | 4/6 | 2262 |

## collatz — integer arithmetic + tight inner loop  (N=30000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 270.3ms | 65.9× | 6/6 | 298.5ms | 28.2ms | 26.4 MB | 4/6 | 307 |
| elixir | 65.0ms | 15.9× | 3/6 | 323.9ms | 258.9ms | 82.5 MB | 6/6 | 307 |
| python | 260.9ms | 63.6× | 5/6 | 271.3ms | 10.4ms | 9.8 MB | 1/6 | 307 |
| node | 7.1ms | 1.7× | 2/6 | 25.4ms | 18.3ms | 48.5 MB | 5/6 | 307 |
| ruby | 82.6ms | 20.1× | 4/6 | 126.6ms | 44.0ms | 23.5 MB | 2/6 | 307 |
| dotnet | 4.1ms | 1.0× | 1/6 | 26.2ms | 22.1ms | 26.1 MB | 3/6 | 307 |

## mandelbrot — floating-point math (escape iterations)  (N=128)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 73.4ms | 66.7× | 5/6 | 101.6ms | 28.2ms | 14.2 MB | 2/6 | 345426 |
| elixir | 63.4ms | 57.6× | 4/6 | 322.3ms | 258.9ms | 80.5 MB | 6/6 | 345426 |
| python | 75.4ms | 68.5× | 6/6 | 85.8ms | 10.4ms | 10.1 MB | 1/6 | 345426 |
| node | 3.1ms | 2.8× | 2/6 | 21.4ms | 18.3ms | 50.2 MB | 5/6 | 345426 |
| ruby | 21.1ms | 19.2× | 3/6 | 65.1ms | 44.0ms | 23.7 MB | 3/6 | 345426 |
| dotnet | 1.1ms | 1.0× | 1/6 | 23.2ms | 22.1ms | 26.1 MB | 4/6 | 345426 |

## matmul — nested loops + indexing (integer NxN)  (N=80)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 670.0ms | 372.2× | 6/6 | 698.2ms | 28.2ms | 28.3 MB | 4/6 | 229499993 |
| elixir | 15.4ms | 8.6× | 3/6 | 274.3ms | 258.9ms | 78.0 MB | 6/6 | 229499993 |
| python | 50.3ms | 27.9× | 5/6 | 60.7ms | 10.4ms | 9.9 MB | 1/6 | 229499993 |
| node | 2.2ms | 1.2× | 2/6 | 20.5ms | 18.3ms | 49.1 MB | 5/6 | 229499993 |
| ruby | 28.8ms | 16.0× | 4/6 | 72.8ms | 44.0ms | 23.7 MB | 2/6 | 229499993 |
| dotnet | 1.8ms | 1.0× | 1/6 | 23.9ms | 22.1ms | 26.3 MB | 3/6 | 229499993 |

## strings — string building (join) + length  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 140.7ms | 35.2× | 6/6 | 168.9ms | 28.2ms | 44.8 MB | 4/6 | 288889 |
| elixir | 17.0ms | 4.2× | 5/6 | 275.9ms | 258.9ms | 89.1 MB | 6/6 | 288889 |
| python | 4.0ms | 1.0× | 1/6 | 14.4ms | 10.4ms | 12.9 MB | 1/6 | 288889 |
| node | 6.1ms | 1.5× | 4/6 | 24.4ms | 18.3ms | 52.5 MB | 5/6 | 288889 |
| ruby | 4.4ms | 1.1× | 2/6 | 48.4ms | 44.0ms | 25.8 MB | 2/6 | 288889 |
| dotnet | 4.6ms | 1.1× | 3/6 | 26.7ms | 22.1ms | 30.1 MB | 3/6 | 288889 |

## wordcount — hash-map build (immutable vs mutable)  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 211.7ms | 33.6× | 6/6 | 239.9ms | 28.2ms | 37.8 MB | 4/6 | 50038280 |
| elixir | 35.4ms | 5.6× | 5/6 | 294.3ms | 258.9ms | 78.3 MB | 6/6 | 50038280 |
| python | 24.6ms | 3.9× | 4/6 | 35.0ms | 10.4ms | 9.9 MB | 1/6 | 50038280 |
| node | 6.9ms | 1.1× | 2/6 | 25.2ms | 18.3ms | 50.3 MB | 5/6 | 50038280 |
| ruby | 6.3ms | 1.0× | 1/6 | 50.3ms | 44.0ms | 23.5 MB | 2/6 | 50038280 |
| dotnet | 10.0ms | 1.6× | 3/6 | 32.1ms | 22.1ms | 27.2 MB | 3/6 | 50038280 |

## bintree — allocation / GC pressure (build+walk trees)  (N=40)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 401.5ms | 100.4× | 6/6 | 429.7ms | 28.2ms | 19.7 MB | 2/6 | 327640 |
| elixir | 49.4ms | 12.4× | 5/6 | 308.3ms | 258.9ms | 81.1 MB | 6/6 | 327640 |
| python | 18.7ms | 4.7× | 3/6 | 29.1ms | 10.4ms | 10.0 MB | 1/6 | 327640 |
| node | 6.0ms | 1.5× | 2/6 | 24.3ms | 18.3ms | 52.3 MB | 5/6 | 327640 |
| ruby | 20.0ms | 5.0× | 4/6 | 64.0ms | 44.0ms | 23.8 MB | 3/6 | 327640 |
| dotnet | 4.0ms | 1.0× | 1/6 | 26.1ms | 22.1ms | 30.8 MB | 4/6 | 327640 |

## sort — sort a list of ints + checksum walk  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 32.5ms | 4.6× | 6/6 | 60.7ms | 28.2ms | 21.4 MB | 2/6 | 102632633 |
| elixir | 22.3ms | 3.1× | 5/6 | 281.2ms | 258.9ms | 86.6 MB | 6/6 | 102632633 |
| python | 19.8ms | 2.8× | 4/6 | 30.2ms | 10.4ms | 12.1 MB | 1/6 | 102632633 |
| node | 15.7ms | 2.2× | 3/6 | 34.0ms | 18.3ms | 51.5 MB | 5/6 | 102632633 |
| ruby | 7.1ms | 1.0× | 1/6 | 51.1ms | 44.0ms | 24.0 MB | 3/6 | 102632633 |
| dotnet | 12.1ms | 1.7× | 2/6 | 34.2ms | 22.1ms | 27.1 MB | 4/6 | 102632633 |

## spawn — lightweight concurrent units + result collection  (N=20000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 1.359s | 66.9× | 4/6 | 1.387s | 28.2ms | 185.9 MB | 5/6 | 12200000 |
| elixir | 97.1ms | 4.8× | 2/6 | 356.0ms | 258.9ms | 90.0 MB | 4/6 | 12200000 |
| python | 1.365s | 67.3× | 5/6 | 1.376s | 10.4ms | 35.9 MB | 2/6 | 12200000 |
| node | 106.0ms | 5.2× | 3/6 | 124.3ms | 18.3ms | 55.8 MB | 3/6 | 12200000 |
| ruby | 4.846s | 238.7× | 6/6 | 4.890s | 44.0ms | 246.4 MB | 6/6 | 12200000 |
| dotnet | 20.3ms | 1.0× | 1/6 | 42.4ms | 22.1ms | 31.6 MB | 1/6 | 12200000 |

## pfib — parallel fib — 100 computed at once across cores  (N=28)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 2.254s | 57.4× | 6/6 | 2.283s | 28.2ms | 14.6 MB | 1/6 | 31781100 |
| elixir | 127.3ms | 3.2× | 2/6 | 386.2ms | 258.9ms | 82.4 MB | 5/6 | 31781100 |
| python | 758.5ms | 19.3× | 5/6 | 768.9ms | 10.4ms | 22.0 MB | 2/6 | 31781100 |
| node | 130.5ms | 3.3× | 3/6 | 148.8ms | 18.3ms | 181.9 MB | 6/6 | 31781100 |
| ruby | 487.5ms | 12.4× | 4/6 | 531.5ms | 44.0ms | 23.7 MB | 3/6 | 31781100 |
| dotnet | 39.3ms | 1.0× | 1/6 | 61.4ms | 22.1ms | 28.0 MB | 4/6 | 31781100 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 147.7ms | 1.5× | 3/5 | 175.9ms | 28.2ms | 75.5 MB | 4/5 | 0 |
| elixir | 628.2ms | 6.2× | 5/5 | 887.1ms | 258.9ms | 529.3 MB | 5/5 | 0 |
| python | — | — | — | — | — | — | — | ERROR |
| node | 111.5ms | 1.1× | 2/5 | 129.8ms | 18.3ms | 64.8 MB | 3/5 | 0 |
| ruby | 196.7ms | 1.9× | 4/5 | 240.7ms | 44.0ms | 50.6 MB | 2/5 | 0 |
| dotnet | 101.4ms | 1.0× | 1/5 | 123.5ms | 22.1ms | 47.9 MB | 1/5 | 0 |
