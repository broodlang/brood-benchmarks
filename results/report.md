# Brood vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-22-generic-x86_64-with-glibc2.43 — 2026-06-08 19:21.
> **Runtimes:** Brood brood 0.1.0; Elixir Elixir 1.20.0-rc.4 (e39a1ca) (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.108.

_startup: best of 1; others: best of 3 runs; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 30.9ms | 2.7× | 4/6 | 30.9ms | — | 12.1 MB | 2/6 | 0 |
| elixir | 308.7ms | 26.8× | 6/6 | 308.7ms | — | 76.3 MB | 6/6 | 0 |
| python | 11.5ms | 1.0× | 1/6 | 11.5ms | — | 9.8 MB | 1/6 | 0 |
| node | 19.3ms | 1.7× | 2/6 | 19.3ms | — | 44.7 MB | 5/6 | 0 |
| ruby | 48.5ms | 4.2× | 5/6 | 48.5ms | — | 23.5 MB | 3/6 | 0 |
| dotnet | 23.1ms | 2.0× | 3/6 | 23.1ms | — | 25.6 MB | 4/6 | 0 |

## fib — naive recursion / function-call overhead  (N=30)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 286.1ms | 92.3× | 6/6 | 317.0ms | 30.9ms | 12.1 MB | 2/6 | 832040 |
| elixir | 28.5ms | 9.2× | 3/6 | 337.2ms | 308.7ms | 84.6 MB | 6/6 | 832040 |
| python | 72.8ms | 23.5× | 5/6 | 84.3ms | 11.5ms | 9.8 MB | 1/6 | 832040 |
| node | 8.9ms | 2.9× | 2/6 | 28.2ms | 19.3ms | 50.3 MB | 5/6 | 832040 |
| ruby | 60.5ms | 19.5× | 4/6 | 109.0ms | 48.5ms | 23.5 MB | 3/6 | 832040 |
| dotnet | 3.1ms | 1.0× | 1/6 | 26.2ms | 23.1ms | 25.7 MB | 4/6 | 832040 |

## loop — raw iteration (tail recursion vs for-loop)  (N=3000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 302.0ms | 302.0× | 6/6 | 332.9ms | 30.9ms | 12.1 MB | 2/6 | 3000000 |
| elixir | 0.0ms | < 1× | 1/6 | 308.5ms | 308.7ms | 80.5 MB | 6/6 | 3000000 |
| python | 209.3ms | 209.3× | 5/6 | 220.8ms | 11.5ms | 9.8 MB | 1/6 | 3000000 |
| node | 2.1ms | 2.1× | 3/6 | 21.4ms | 19.3ms | 50.1 MB | 5/6 | 3000000 |
| ruby | 61.6ms | 61.6× | 4/6 | 110.1ms | 48.5ms | 23.4 MB | 3/6 | 3000000 |
| dotnet | 0.6ms | < 1× | 2/6 | 23.7ms | 23.1ms | 26.1 MB | 4/6 | 3000000 |

## reduce — higher-order fold over a range  (N=1000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 86.6ms | 86.6× | 6/6 | 117.5ms | 30.9ms | 12.0 MB | 2/6 | 499999500000 |
| elixir | 0.0ms | < 1× | 1/6 | 279.3ms | 308.7ms | 81.0 MB | 6/6 | 499999500000 |
| python | 5.9ms | 5.9× | 5/6 | 17.4ms | 11.5ms | 9.7 MB | 1/6 | 499999500000 |
| node | 2.5ms | 2.5× | 4/6 | 21.8ms | 19.3ms | 52.0 MB | 5/6 | 499999500000 |
| ruby | 0.0ms | < 1× | 2/6 | 44.1ms | 48.5ms | 23.5 MB | 3/6 | 499999500000 |
| dotnet | 1.0ms | 1.0× | 3/6 | 24.1ms | 23.1ms | 26.1 MB | 4/6 | 499999500000 |

## primes — integer arithmetic (trial division)  (N=20000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 39.5ms | 39.5× | 6/6 | 70.4ms | 30.9ms | 12.2 MB | 2/6 | 2262 |
| elixir | 19.1ms | 19.1× | 5/6 | 327.8ms | 308.7ms | 81.3 MB | 6/6 | 2262 |
| python | 8.3ms | 8.3× | 4/6 | 19.8ms | 11.5ms | 9.9 MB | 1/6 | 2262 |
| node | 0.7ms | < 1× | 1/6 | 20.0ms | 19.3ms | 50.8 MB | 5/6 | 2262 |
| ruby | 2.7ms | 2.7× | 3/6 | 51.2ms | 48.5ms | 23.5 MB | 3/6 | 2262 |
| dotnet | 1.1ms | 1.1× | 2/6 | 24.2ms | 23.1ms | 26.1 MB | 4/6 | 2262 |

## collatz — integer arithmetic + tight inner loop  (N=30000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 484.3ms | 124.2× | 6/6 | 515.2ms | 30.9ms | 20.0 MB | 2/6 | 307 |
| elixir | 20.7ms | 5.3× | 3/6 | 329.4ms | 308.7ms | 81.2 MB | 6/6 | 307 |
| python | 258.6ms | 66.3× | 5/6 | 270.1ms | 11.5ms | 9.8 MB | 1/6 | 307 |
| node | 8.9ms | 2.3× | 2/6 | 28.2ms | 19.3ms | 50.3 MB | 5/6 | 307 |
| ruby | 84.6ms | 21.7× | 4/6 | 133.1ms | 48.5ms | 23.5 MB | 3/6 | 307 |
| dotnet | 3.9ms | 1.0× | 1/6 | 27.0ms | 23.1ms | 26.0 MB | 4/6 | 307 |

## mandelbrot — floating-point math (escape iterations)  (N=128)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 99.6ms | 90.5× | 6/6 | 130.5ms | 30.9ms | 12.2 MB | 2/6 | 345426 |
| elixir | 19.0ms | 17.3× | 3/6 | 327.7ms | 308.7ms | 80.7 MB | 6/6 | 345426 |
| python | 77.5ms | 70.5× | 5/6 | 89.0ms | 11.5ms | 10.1 MB | 1/6 | 345426 |
| node | 2.4ms | 2.2× | 2/6 | 21.7ms | 19.3ms | 52.1 MB | 5/6 | 345426 |
| ruby | 26.0ms | 23.6× | 4/6 | 74.5ms | 48.5ms | 23.6 MB | 3/6 | 345426 |
| dotnet | 1.1ms | 1.0× | 1/6 | 24.2ms | 23.1ms | 26.1 MB | 4/6 | 345426 |

## matmul — nested loops + indexing (integer NxN)  (N=80)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 615.3ms | 615.3× | 6/6 | 646.2ms | 30.9ms | 20.1 MB | 2/6 | 229499993 |
| elixir | 0.0ms | < 1× | 1/6 | 280.6ms | 308.7ms | 81.4 MB | 6/6 | 229499993 |
| python | 47.9ms | 47.9× | 5/6 | 59.4ms | 11.5ms | 9.9 MB | 1/6 | 229499993 |
| node | 3.1ms | 3.1× | 3/6 | 22.4ms | 19.3ms | 50.5 MB | 5/6 | 229499993 |
| ruby | 29.3ms | 29.3× | 4/6 | 77.8ms | 48.5ms | 23.5 MB | 3/6 | 229499993 |
| dotnet | 0.1ms | < 1× | 2/6 | 23.2ms | 23.1ms | 26.2 MB | 4/6 | 229499993 |

## strings — string building (join) + length  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 127.7ms | 127.7× | 6/6 | 158.6ms | 30.9ms | 36.1 MB | 4/6 | 288889 |
| elixir | 0.0ms | < 1× | 1/6 | 290.3ms | 308.7ms | 88.9 MB | 6/6 | 288889 |
| python | 3.4ms | 3.4× | 3/6 | 14.9ms | 11.5ms | 12.8 MB | 1/6 | 288889 |
| node | 5.9ms | 5.9× | 5/6 | 25.2ms | 19.3ms | 54.5 MB | 5/6 | 288889 |
| ruby | 4.8ms | 4.8× | 4/6 | 53.3ms | 48.5ms | 25.8 MB | 2/6 | 288889 |
| dotnet | 3.4ms | 3.4× | 2/6 | 26.5ms | 23.1ms | 30.0 MB | 3/6 | 288889 |

## wordcount — hash-map build (immutable vs mutable)  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 183.7ms | 31.7× | 6/6 | 214.6ms | 30.9ms | 28.5 MB | 4/6 | 50038280 |
| elixir | 10.0ms | 1.7× | 4/6 | 318.7ms | 308.7ms | 78.4 MB | 6/6 | 50038280 |
| python | 24.7ms | 4.3× | 5/6 | 36.2ms | 11.5ms | 10.0 MB | 1/6 | 50038280 |
| node | 6.0ms | 1.0× | 2/6 | 25.3ms | 19.3ms | 52.4 MB | 5/6 | 50038280 |
| ruby | 5.8ms | 1.0× | 1/6 | 54.3ms | 48.5ms | 23.5 MB | 2/6 | 50038280 |
| dotnet | 8.5ms | 1.5× | 3/6 | 31.6ms | 23.1ms | 27.2 MB | 3/6 | 50038280 |

## bintree — allocation / GC pressure (build+walk trees)  (N=40)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 343.3ms | 343.3× | 6/6 | 374.2ms | 30.9ms | 16.2 MB | 2/6 | 327640 |
| elixir | 0.0ms | < 1× | 1/6 | 304.4ms | 308.7ms | 84.0 MB | 6/6 | 327640 |
| python | 19.8ms | 19.8× | 5/6 | 31.3ms | 11.5ms | 10.0 MB | 1/6 | 327640 |
| node | 5.2ms | 5.2× | 3/6 | 24.5ms | 19.3ms | 54.1 MB | 5/6 | 327640 |
| ruby | 14.8ms | 14.8× | 4/6 | 63.3ms | 48.5ms | 23.8 MB | 3/6 | 327640 |
| dotnet | 4.9ms | 4.9× | 2/6 | 28.0ms | 23.1ms | 30.8 MB | 4/6 | 327640 |

## sort — sort a list of ints + checksum walk  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 28.6ms | 28.6× | 6/6 | 59.5ms | 30.9ms | 16.8 MB | 2/6 | 102632633 |
| elixir | 0.0ms | < 1× | 1/6 | 285.6ms | 308.7ms | 88.1 MB | 6/6 | 102632633 |
| python | 19.1ms | 19.1× | 5/6 | 30.6ms | 11.5ms | 12.2 MB | 1/6 | 102632633 |
| node | 16.5ms | 16.5× | 4/6 | 35.8ms | 19.3ms | 53.2 MB | 5/6 | 102632633 |
| ruby | 3.5ms | 3.5× | 2/6 | 52.0ms | 48.5ms | 24.0 MB | 3/6 | 102632633 |
| dotnet | 12.7ms | 12.7× | 3/6 | 35.8ms | 23.1ms | 27.1 MB | 4/6 | 102632633 |

## spawn — lightweight concurrent units + result collection  (N=20000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 1.056s | 48.4× | 4/6 | 1.087s | 30.9ms | 162.9 MB | 5/6 | 12200000 |
| elixir | 59.8ms | 2.7× | 2/6 | 368.5ms | 308.7ms | 91.5 MB | 4/6 | 12200000 |
| python | 1.079s | 49.5× | 5/6 | 1.090s | 11.5ms | 35.9 MB | 2/6 | 12200000 |
| node | 102.3ms | 4.7× | 3/6 | 121.6ms | 19.3ms | 57.6 MB | 3/6 | 12200000 |
| ruby | 4.951s | 227.1× | 6/6 | 5.000s | 48.5ms | 246.8 MB | 6/6 | 12200000 |
| dotnet | 21.8ms | 1.0× | 1/6 | 44.9ms | 23.1ms | 31.9 MB | 1/6 | 12200000 |

## pfib — parallel fib — 100 computed at once across cores  (N=28)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 2.240s | 55.7× | 6/6 | 2.271s | 30.9ms | 12.2 MB | 1/6 | 31781100 |
| elixir | 110.5ms | 2.7× | 2/6 | 419.2ms | 308.7ms | 81.7 MB | 5/6 | 31781100 |
| python | 776.9ms | 19.3× | 5/6 | 788.4ms | 11.5ms | 22.4 MB | 2/6 | 31781100 |
| node | 148.4ms | 3.7× | 3/6 | 167.7ms | 19.3ms | 185.2 MB | 6/6 | 31781100 |
| ruby | 582.6ms | 14.5× | 4/6 | 631.1ms | 48.5ms | 23.7 MB | 3/6 | 31781100 |
| dotnet | 40.2ms | 1.0× | 1/6 | 63.3ms | 23.1ms | 28.0 MB | 4/6 | 31781100 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 161.5ms | 1.3× | 3/6 | 192.4ms | 30.9ms | 85.1 MB | 5/6 | 500 |
| elixir | 732.7ms | 5.9× | 6/6 | 1.041s | 308.7ms | 591.3 MB | 6/6 | 500 |
| python | 186.6ms | 1.5× | 4/6 | 198.1ms | 11.5ms | 45.7 MB | 1/6 | 500 |
| node | 124.4ms | 1.0× | 1/6 | 143.7ms | 19.3ms | 67.2 MB | 4/6 | 500 |
| ruby | 223.2ms | 1.8× | 5/6 | 271.7ms | 48.5ms | 50.3 MB | 3/6 | 500 |
| dotnet | 160.3ms | 1.3× | 2/6 | 183.4ms | 23.1ms | 48.1 MB | 2/6 | 500 |
