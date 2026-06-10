# Brood vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-22-generic-x86_64-with-glibc2.43 — 2026-06-10 19:10.
> **Runtimes:** Brood brood 0.1.0; Elixir Elixir 1.20.0 (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.108.

_best of 3 runs; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 28.2ms | 2.9× | 4/6 | 28.2ms | — | 14.2 MB | 2/6 | 0 |
| elixir | 255.6ms | 26.4× | 6/6 | 255.6ms | — | 78.6 MB | 6/6 | 0 |
| python | 9.7ms | 1.0× | 1/6 | 9.7ms | — | 9.8 MB | 1/6 | 0 |
| node | 18.1ms | 1.9× | 2/6 | 18.1ms | — | 43.2 MB | 5/6 | 0 |
| ruby | 42.6ms | 4.4× | 5/6 | 42.6ms | — | 23.5 MB | 3/6 | 0 |
| dotnet | 21.5ms | 2.2× | 3/6 | 21.5ms | — | 25.7 MB | 4/6 | 0 |

## fib — naive recursion / function-call overhead  (N=30)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 230.0ms | 54.8× | 6/6 | 258.2ms | 28.2ms | 14.1 MB | 2/6 | 832040 |
| elixir | 64.8ms | 15.4× | 4/6 | 320.4ms | 255.6ms | 80.7 MB | 6/6 | 832040 |
| python | 66.5ms | 15.8× | 5/6 | 76.2ms | 9.7ms | 9.8 MB | 1/6 | 832040 |
| node | 8.5ms | 2.0× | 2/6 | 26.6ms | 18.1ms | 48.5 MB | 5/6 | 832040 |
| ruby | 54.0ms | 12.9× | 3/6 | 96.6ms | 42.6ms | 23.5 MB | 3/6 | 832040 |
| dotnet | 4.2ms | 1.0× | 1/6 | 25.7ms | 21.5ms | 25.6 MB | 4/6 | 832040 |

## loop — raw iteration (tail recursion vs for-loop)  (N=3000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 142.5ms | 59.4× | 5/6 | 170.7ms | 28.2ms | 14.3 MB | 2/6 | 3000000 |
| elixir | 58.3ms | 24.3× | 3/6 | 313.9ms | 255.6ms | 81.2 MB | 6/6 | 3000000 |
| python | 194.2ms | 80.9× | 6/6 | 203.9ms | 9.7ms | 9.7 MB | 1/6 | 3000000 |
| node | 3.2ms | 1.3× | 2/6 | 21.3ms | 18.1ms | 48.4 MB | 5/6 | 3000000 |
| ruby | 60.7ms | 25.3× | 4/6 | 103.3ms | 42.6ms | 23.5 MB | 3/6 | 3000000 |
| dotnet | 2.4ms | 1.0× | 1/6 | 23.9ms | 21.5ms | 26.1 MB | 4/6 | 3000000 |

## reduce — higher-order fold over a range  (N=1000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 20.9ms | 20.9× | 6/6 | 49.1ms | 28.2ms | 14.1 MB | 2/6 | 499999500000 |
| elixir | 11.6ms | 11.6× | 5/6 | 267.2ms | 255.6ms | 78.6 MB | 6/6 | 499999500000 |
| python | 7.2ms | 7.2× | 4/6 | 16.9ms | 9.7ms | 9.8 MB | 1/6 | 499999500000 |
| node | 2.6ms | 2.6× | 3/6 | 20.7ms | 18.1ms | 50.3 MB | 5/6 | 499999500000 |
| ruby | 0.6ms | < 1× | 1/6 | 43.2ms | 42.6ms | 23.5 MB | 3/6 | 499999500000 |
| dotnet | 1.7ms | 1.7× | 2/6 | 23.2ms | 21.5ms | 26.0 MB | 4/6 | 499999500000 |

## primes — integer arithmetic (trial division)  (N=20000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 25.4ms | 12.7× | 5/6 | 53.6ms | 28.2ms | 14.2 MB | 2/6 | 2262 |
| elixir | 51.7ms | 25.9× | 6/6 | 307.3ms | 255.6ms | 80.7 MB | 6/6 | 2262 |
| python | 9.8ms | 4.9× | 4/6 | 19.5ms | 9.7ms | 9.9 MB | 1/6 | 2262 |
| node | 2.0ms | 1.0× | 1/6 | 20.1ms | 18.1ms | 49.1 MB | 5/6 | 2262 |
| ruby | 6.6ms | 3.3× | 3/6 | 49.2ms | 42.6ms | 23.5 MB | 3/6 | 2262 |
| dotnet | 2.2ms | 1.1× | 2/6 | 23.7ms | 21.5ms | 26.1 MB | 4/6 | 2262 |

## collatz — integer arithmetic + tight inner loop  (N=30000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 301.2ms | 61.5× | 6/6 | 329.4ms | 28.2ms | 26.8 MB | 4/6 | 307 |
| elixir | 57.3ms | 11.7× | 3/6 | 312.9ms | 255.6ms | 81.9 MB | 6/6 | 307 |
| python | 232.2ms | 47.4× | 5/6 | 241.9ms | 9.7ms | 9.8 MB | 1/6 | 307 |
| node | 8.1ms | 1.7× | 2/6 | 26.2ms | 18.1ms | 48.6 MB | 5/6 | 307 |
| ruby | 81.6ms | 16.7× | 4/6 | 124.2ms | 42.6ms | 23.5 MB | 2/6 | 307 |
| dotnet | 4.9ms | 1.0× | 1/6 | 26.4ms | 21.5ms | 26.0 MB | 3/6 | 307 |

## mandelbrot — floating-point math (escape iterations)  (N=128)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 73.9ms | 24.6× | 5/6 | 102.1ms | 28.2ms | 14.2 MB | 2/6 | 345426 |
| elixir | 55.8ms | 18.6× | 4/6 | 311.4ms | 255.6ms | 80.6 MB | 6/6 | 345426 |
| python | 82.3ms | 27.4× | 6/6 | 92.0ms | 9.7ms | 10.1 MB | 1/6 | 345426 |
| node | 4.8ms | 1.6× | 2/6 | 22.9ms | 18.1ms | 50.6 MB | 5/6 | 345426 |
| ruby | 30.4ms | 10.1× | 3/6 | 73.0ms | 42.6ms | 23.7 MB | 3/6 | 345426 |
| dotnet | 3.0ms | 1.0× | 1/6 | 24.5ms | 21.5ms | 26.0 MB | 4/6 | 345426 |

## matmul — nested loops + indexing (integer NxN)  (N=80)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 152.9ms | 69.5× | 6/6 | 181.1ms | 28.2ms | 28.3 MB | 4/6 | 229499993 |
| elixir | 27.3ms | 12.4× | 4/6 | 282.9ms | 255.6ms | 80.1 MB | 6/6 | 229499993 |
| python | 42.8ms | 19.5× | 5/6 | 52.5ms | 9.7ms | 9.9 MB | 1/6 | 229499993 |
| node | 2.8ms | 1.3× | 2/6 | 20.9ms | 18.1ms | 49.2 MB | 5/6 | 229499993 |
| ruby | 27.2ms | 12.4× | 3/6 | 69.8ms | 42.6ms | 23.7 MB | 2/6 | 229499993 |
| dotnet | 2.2ms | 1.0× | 1/6 | 23.7ms | 21.5ms | 26.1 MB | 3/6 | 229499993 |

## strings — string building (join) + length  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 63.5ms | 12.2× | 6/6 | 91.7ms | 28.2ms | 29.7 MB | 3/6 | 288889 |
| elixir | 25.5ms | 4.9× | 5/6 | 281.1ms | 255.6ms | 86.6 MB | 6/6 | 288889 |
| python | 5.2ms | 1.0× | 1/6 | 14.9ms | 9.7ms | 12.8 MB | 1/6 | 288889 |
| node | 6.6ms | 1.3× | 3/6 | 24.7ms | 18.1ms | 52.5 MB | 5/6 | 288889 |
| ruby | 7.5ms | 1.4× | 4/6 | 50.1ms | 42.6ms | 25.8 MB | 2/6 | 288889 |
| dotnet | 5.7ms | 1.1× | 2/6 | 27.2ms | 21.5ms | 30.0 MB | 4/6 | 288889 |

## wordcount — hash-map build (immutable vs mutable)  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 162.0ms | 22.8× | 6/6 | 190.2ms | 28.2ms | 53.6 MB | 5/6 | 50038280 |
| elixir | 41.6ms | 5.9× | 5/6 | 297.2ms | 255.6ms | 78.2 MB | 6/6 | 50038280 |
| python | 23.4ms | 3.3× | 4/6 | 33.1ms | 9.7ms | 9.9 MB | 1/6 | 50038280 |
| node | 7.1ms | 1.0× | 1/6 | 25.2ms | 18.1ms | 50.4 MB | 4/6 | 50038280 |
| ruby | 8.1ms | 1.1× | 2/6 | 50.7ms | 42.6ms | 23.5 MB | 2/6 | 50038280 |
| dotnet | 9.9ms | 1.4× | 3/6 | 31.4ms | 21.5ms | 27.2 MB | 3/6 | 50038280 |

## bintree — allocation / GC pressure (build+walk trees)  (N=40)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 338.7ms | 69.1× | 6/6 | 366.9ms | 28.2ms | 22.1 MB | 2/6 | 327640 |
| elixir | 59.9ms | 12.2× | 5/6 | 315.5ms | 255.6ms | 80.8 MB | 6/6 | 327640 |
| python | 21.5ms | 4.4× | 4/6 | 31.2ms | 9.7ms | 10.0 MB | 1/6 | 327640 |
| node | 6.8ms | 1.4× | 2/6 | 24.9ms | 18.1ms | 52.3 MB | 5/6 | 327640 |
| ruby | 18.9ms | 3.9× | 3/6 | 61.5ms | 42.6ms | 23.8 MB | 3/6 | 327640 |
| dotnet | 4.9ms | 1.0× | 1/6 | 26.4ms | 21.5ms | 30.7 MB | 4/6 | 327640 |

## sort — sort a list of ints + checksum walk  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 36.0ms | 4.1× | 6/6 | 64.2ms | 28.2ms | 21.3 MB | 2/6 | 102632633 |
| elixir | 29.6ms | 3.4× | 5/6 | 285.2ms | 255.6ms | 86.4 MB | 6/6 | 102632633 |
| python | 18.7ms | 2.1× | 4/6 | 28.4ms | 9.7ms | 12.2 MB | 1/6 | 102632633 |
| node | 15.5ms | 1.8× | 3/6 | 33.6ms | 18.1ms | 51.5 MB | 5/6 | 102632633 |
| ruby | 8.8ms | 1.0× | 1/6 | 51.4ms | 42.6ms | 24.2 MB | 3/6 | 102632633 |
| dotnet | 13.9ms | 1.6× | 2/6 | 35.4ms | 21.5ms | 27.1 MB | 4/6 | 102632633 |

## spawn — lightweight concurrent units + result collection  (N=20000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 1.332s | 64.0× | 5/6 | 1.360s | 28.2ms | 182.6 MB | 5/6 | 12200000 |
| elixir | 83.4ms | 4.0× | 2/6 | 339.0ms | 255.6ms | 90.4 MB | 4/6 | 12200000 |
| python | 1.063s | 51.1× | 4/6 | 1.073s | 9.7ms | 36.0 MB | 2/6 | 12200000 |
| node | 105.3ms | 5.1× | 3/6 | 123.4ms | 18.1ms | 55.9 MB | 3/6 | 12200000 |
| ruby | 4.932s | 237.1× | 6/6 | 4.975s | 42.6ms | 246.7 MB | 6/6 | 12200000 |
| dotnet | 20.8ms | 1.0× | 1/6 | 42.3ms | 21.5ms | 32.0 MB | 1/6 | 12200000 |

## pfib — parallel fib — 100 computed at once across cores  (N=28)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 2.269s | 56.6× | 6/6 | 2.297s | 28.2ms | 14.5 MB | 1/6 | 31781100 |
| elixir | 128.9ms | 3.2× | 3/6 | 384.5ms | 255.6ms | 85.1 MB | 5/6 | 31781100 |
| python | 757.8ms | 18.9× | 5/6 | 767.5ms | 9.7ms | 22.3 MB | 2/6 | 31781100 |
| node | 128.5ms | 3.2× | 2/6 | 146.6ms | 18.1ms | 181.7 MB | 6/6 | 31781100 |
| ruby | 493.8ms | 12.3× | 4/6 | 536.4ms | 42.6ms | 23.7 MB | 3/6 | 31781100 |
| dotnet | 40.1ms | 1.0× | 1/6 | 61.6ms | 21.5ms | 28.1 MB | 4/6 | 31781100 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 186.5ms | 1.5× | 4/6 | 214.7ms | 28.2ms | 101.0 MB | 5/6 | 500 |
| elixir | 747.5ms | 5.9× | 6/6 | 1.003s | 255.6ms | 543.0 MB | 6/6 | 500 |
| python | 181.7ms | 1.4× | 3/6 | 191.4ms | 9.7ms | 47.0 MB | 1/6 | 500 |
| node | 126.7ms | 1.0× | 1/6 | 144.8ms | 18.1ms | 65.3 MB | 4/6 | 500 |
| ruby | 200.3ms | 1.6× | 5/6 | 242.9ms | 42.6ms | 50.0 MB | 3/6 | 500 |
| dotnet | 151.5ms | 1.2× | 2/6 | 173.0ms | 21.5ms | 48.0 MB | 2/6 | 500 |
