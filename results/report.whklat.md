# Brood vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-22-generic-x86_64-with-glibc2.43 — 2026-06-08 08:58.
> **Runtimes:** Brood brood 0.1.0; Elixir Elixir 1.20.0-rc.4 (e39a1ca) (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.108.

_Best of 3 runs per program; full sizes. **wall = startup + compute.** `startup` is that language's own boot time (its `startup`-row wall); `compute` = wall − startup, so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself compute is ~0 by definition. RSS = peak resident memory. `pos` = rank by wall, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | wall | startup | compute | vs fastest | pos | peak RSS | mem | checksum |
|------|------|---------|---------|-----------|-----|----------|-----|----------|
| brood | 29.4ms | 29.4ms | 0.0ms | 2.3× | 4/6 | 11.8 MB | 2/6 | 0 |
| elixir | 326.2ms | 326.2ms | 0.0ms | 25.1× | 6/6 | 76.1 MB | 6/6 | 0 |
| python | 13.0ms | 13.0ms | 0.0ms | 1.0× | 1/6 | 9.8 MB | 1/6 | 0 |
| node | 21.3ms | 21.3ms | 0.0ms | 1.6× | 2/6 | 44.7 MB | 5/6 | 0 |
| ruby | 57.7ms | 57.7ms | 0.0ms | 4.4× | 5/6 | 23.5 MB | 3/6 | 0 |
| dotnet | 24.1ms | 24.1ms | 0.0ms | 1.9× | 3/6 | 25.6 MB | 4/6 | 0 |

## fib — naive recursion / function-call overhead  (N=30)

| lang | wall | startup | compute | vs fastest | pos | peak RSS | mem | checksum |
|------|------|---------|---------|-----------|-----|----------|-----|----------|
| brood | 301.7ms | 29.4ms | 272.3ms | 10.8× | 5/6 | 12.1 MB | 2/6 | 832040 |
| elixir | 387.9ms | 326.2ms | 61.7ms | 13.9× | 6/6 | 81.0 MB | 6/6 | 832040 |
| python | 103.1ms | 13.0ms | 90.1ms | 3.7× | 3/6 | 9.8 MB | 1/6 | 832040 |
| node | 31.8ms | 21.3ms | 10.5ms | 1.1× | 2/6 | 50.3 MB | 5/6 | 832040 |
| ruby | 119.2ms | 57.7ms | 61.5ms | 4.3× | 4/6 | 23.5 MB | 3/6 | 832040 |
| dotnet | 27.9ms | 24.1ms | 3.8ms | 1.0× | 1/6 | 25.7 MB | 4/6 | 832040 |

## loop — raw iteration (tail recursion vs for-loop)  (N=3000000)

| lang | wall | startup | compute | vs fastest | pos | peak RSS | mem | checksum |
|------|------|---------|---------|-----------|-----|----------|-----|----------|
| brood | 366.2ms | 29.4ms | 336.8ms | 16.6× | 6/6 | 12.2 MB | 2/6 | 3000000 |
| elixir | 307.0ms | 326.2ms | 0.0ms | 13.9× | 5/6 | 80.6 MB | 6/6 | 3000000 |
| python | 244.0ms | 13.0ms | 231.0ms | 11.0× | 4/6 | 9.7 MB | 1/6 | 3000000 |
| node | 22.1ms | 21.3ms | 0.8ms | 1.0× | 1/6 | 50.1 MB | 5/6 | 3000000 |
| ruby | 112.3ms | 57.7ms | 54.6ms | 5.1× | 3/6 | 23.5 MB | 3/6 | 3000000 |
| dotnet | 25.2ms | 24.1ms | 1.1ms | 1.1× | 2/6 | 26.1 MB | 4/6 | 3000000 |

## reduce — higher-order fold over a range  (N=1000000)

| lang | wall | startup | compute | vs fastest | pos | peak RSS | mem | checksum |
|------|------|---------|---------|-----------|-----|----------|-----|----------|
| brood | 123.3ms | 29.4ms | 93.9ms | 7.0× | 5/6 | 12.0 MB | 2/6 | 499999500000 |
| elixir | 279.7ms | 326.2ms | 0.0ms | 15.9× | 6/6 | 78.2 MB | 6/6 | 499999500000 |
| python | 17.6ms | 13.0ms | 4.6ms | 1.0× | 1/6 | 9.8 MB | 1/6 | 499999500000 |
| node | 21.1ms | 21.3ms | 0.0ms | 1.2× | 2/6 | 51.9 MB | 5/6 | 499999500000 |
| ruby | 44.7ms | 57.7ms | 0.0ms | 2.5× | 4/6 | 23.5 MB | 3/6 | 499999500000 |
| dotnet | 24.0ms | 24.1ms | 0.0ms | 1.4× | 3/6 | 26.0 MB | 4/6 | 499999500000 |

## primes — integer arithmetic (trial division)  (N=20000)

| lang | wall | startup | compute | vs fastest | pos | peak RSS | mem | checksum |
|------|------|---------|---------|-----------|-----|----------|-----|----------|
| brood | 67.3ms | 29.4ms | 37.9ms | 3.3× | 5/6 | 11.9 MB | 2/6 | 2262 |
| elixir | 311.4ms | 326.2ms | 0.0ms | 15.2× | 6/6 | 80.4 MB | 6/6 | 2262 |
| python | 23.2ms | 13.0ms | 10.2ms | 1.1× | 2/6 | 9.9 MB | 1/6 | 2262 |
| node | 20.5ms | 21.3ms | 0.0ms | 1.0× | 1/6 | 50.8 MB | 5/6 | 2262 |
| ruby | 55.7ms | 57.7ms | 0.0ms | 2.7× | 4/6 | 23.5 MB | 3/6 | 2262 |
| dotnet | 24.7ms | 24.1ms | 0.6ms | 1.2× | 3/6 | 26.1 MB | 4/6 | 2262 |

## collatz — integer arithmetic + tight inner loop  (N=30000)

| lang | wall | startup | compute | vs fastest | pos | peak RSS | mem | checksum |
|------|------|---------|---------|-----------|-----|----------|-----|----------|
| brood | 549.5ms | 29.4ms | 520.1ms | 20.7× | 6/6 | 19.7 MB | 2/6 | 307 |
| elixir | 323.6ms | 326.2ms | 0.0ms | 12.2× | 5/6 | 80.8 MB | 6/6 | 307 |
| python | 293.4ms | 13.0ms | 280.4ms | 11.0× | 4/6 | 9.8 MB | 1/6 | 307 |
| node | 26.6ms | 21.3ms | 5.3ms | 1.0× | 1/6 | 50.2 MB | 5/6 | 307 |
| ruby | 162.9ms | 57.7ms | 105.2ms | 6.1× | 3/6 | 23.5 MB | 3/6 | 307 |
| dotnet | 27.1ms | 24.1ms | 3.0ms | 1.0× | 2/6 | 26.1 MB | 4/6 | 307 |

## mandelbrot — floating-point math (escape iterations)  (N=128)

| lang | wall | startup | compute | vs fastest | pos | peak RSS | mem | checksum |
|------|------|---------|---------|-----------|-----|----------|-----|----------|
| brood | 129.6ms | 29.4ms | 100.2ms | 6.0× | 5/6 | 11.9 MB | 2/6 | 345426 |
| elixir | 328.5ms | 326.2ms | 2.3ms | 15.3× | 6/6 | 81.8 MB | 6/6 | 345426 |
| python | 94.6ms | 13.0ms | 81.6ms | 4.4× | 4/6 | 10.1 MB | 1/6 | 345426 |
| node | 21.5ms | 21.3ms | 0.2ms | 1.0× | 1/6 | 52.5 MB | 5/6 | 345426 |
| ruby | 73.0ms | 57.7ms | 15.3ms | 3.4× | 3/6 | 23.6 MB | 3/6 | 345426 |
| dotnet | 24.5ms | 24.1ms | 0.4ms | 1.1× | 2/6 | 26.0 MB | 4/6 | 345426 |

## matmul — nested loops + indexing (integer NxN)  (N=80)

| lang | wall | startup | compute | vs fastest | pos | peak RSS | mem | checksum |
|------|------|---------|---------|-----------|-----|----------|-----|----------|
| brood | 739.0ms | 29.4ms | 709.6ms | 34.1× | 6/6 | 20.4 MB | 2/6 | 229499993 |
| elixir | 294.3ms | 326.2ms | 0.0ms | 13.6× | 5/6 | 78.1 MB | 6/6 | 229499993 |
| python | 55.2ms | 13.0ms | 42.2ms | 2.5× | 3/6 | 9.9 MB | 1/6 | 229499993 |
| node | 21.7ms | 21.3ms | 0.4ms | 1.0× | 1/6 | 50.9 MB | 5/6 | 229499993 |
| ruby | 72.2ms | 57.7ms | 14.5ms | 3.3× | 4/6 | 23.6 MB | 3/6 | 229499993 |
| dotnet | 24.0ms | 24.1ms | 0.0ms | 1.1× | 2/6 | 26.2 MB | 4/6 | 229499993 |

## strings — string building (join) + length  (N=50000)

| lang | wall | startup | compute | vs fastest | pos | peak RSS | mem | checksum |
|------|------|---------|---------|-----------|-----|----------|-----|----------|
| brood | 179.2ms | 29.4ms | 149.8ms | 11.7× | 5/6 | 35.6 MB | 4/6 | 288889 |
| elixir | 281.1ms | 326.2ms | 0.0ms | 18.4× | 6/6 | 86.5 MB | 6/6 | 288889 |
| python | 15.3ms | 13.0ms | 2.3ms | 1.0× | 1/6 | 12.8 MB | 1/6 | 288889 |
| node | 24.2ms | 21.3ms | 2.9ms | 1.6× | 2/6 | 54.4 MB | 5/6 | 288889 |
| ruby | 50.7ms | 57.7ms | 0.0ms | 3.3× | 4/6 | 25.8 MB | 2/6 | 288889 |
| dotnet | 26.8ms | 24.1ms | 2.7ms | 1.8× | 3/6 | 30.0 MB | 3/6 | 288889 |

## wordcount — hash-map build (immutable vs mutable)  (N=100000)

| lang | wall | startup | compute | vs fastest | pos | peak RSS | mem | checksum |
|------|------|---------|---------|-----------|-----|----------|-----|----------|
| brood | 221.9ms | 29.4ms | 192.5ms | 8.8× | 5/6 | 28.2 MB | 4/6 | 50038280 |
| elixir | 304.7ms | 326.2ms | 0.0ms | 12.1× | 6/6 | 78.4 MB | 6/6 | 50038280 |
| python | 33.5ms | 13.0ms | 20.5ms | 1.3× | 3/6 | 9.9 MB | 1/6 | 50038280 |
| node | 25.1ms | 21.3ms | 3.8ms | 1.0× | 1/6 | 52.3 MB | 5/6 | 50038280 |
| ruby | 58.3ms | 57.7ms | 0.6ms | 2.3× | 4/6 | 23.5 MB | 2/6 | 50038280 |
| dotnet | 32.3ms | 24.1ms | 8.2ms | 1.3× | 2/6 | 27.2 MB | 3/6 | 50038280 |

## bintree — allocation / GC pressure (build+walk trees)  (N=40)

| lang | wall | startup | compute | vs fastest | pos | peak RSS | mem | checksum |
|------|------|---------|---------|-----------|-----|----------|-----|----------|
| brood | 378.0ms | 29.4ms | 348.6ms | 15.2× | 6/6 | 16.0 MB | 2/6 | 327640 |
| elixir | 313.6ms | 326.2ms | 0.0ms | 12.6× | 5/6 | 82.9 MB | 6/6 | 327640 |
| python | 30.2ms | 13.0ms | 17.2ms | 1.2× | 3/6 | 10.0 MB | 1/6 | 327640 |
| node | 24.8ms | 21.3ms | 3.5ms | 1.0× | 1/6 | 54.2 MB | 5/6 | 327640 |
| ruby | 66.2ms | 57.7ms | 8.5ms | 2.7× | 4/6 | 23.8 MB | 3/6 | 327640 |
| dotnet | 27.1ms | 24.1ms | 3.0ms | 1.1× | 2/6 | 30.7 MB | 4/6 | 327640 |

## sort — sort a list of ints + checksum walk  (N=50000)

| lang | wall | startup | compute | vs fastest | pos | peak RSS | mem | checksum |
|------|------|---------|---------|-----------|-----|----------|-----|----------|
| brood | 60.4ms | 29.4ms | 31.0ms | 1.9× | 4/6 | 16.6 MB | 2/6 | 102632633 |
| elixir | 285.1ms | 326.2ms | 0.0ms | 9.0× | 6/6 | 86.1 MB | 6/6 | 102632633 |
| python | 31.7ms | 13.0ms | 18.7ms | 1.0× | 1/6 | 12.1 MB | 1/6 | 102632633 |
| node | 36.0ms | 21.3ms | 14.7ms | 1.1× | 2/6 | 53.3 MB | 5/6 | 102632633 |
| ruby | 63.7ms | 57.7ms | 6.0ms | 2.0× | 5/6 | 24.1 MB | 3/6 | 102632633 |
| dotnet | 40.4ms | 24.1ms | 16.3ms | 1.3× | 3/6 | 27.0 MB | 4/6 | 102632633 |

## spawn — lightweight processes + messaging  (N=20000)

| lang | wall | startup | compute | vs fastest | pos | peak RSS | mem | checksum |
|------|------|---------|---------|-----------|-----|----------|-----|----------|
| brood | 292.5ms | 29.4ms | 263.1ms | 1.0× | 1/2 | 36.3 MB | 1/2 | 199990000 |
| elixir | 332.3ms | 326.2ms | 6.1ms | 1.1× | 2/2 | 91.3 MB | 2/2 | 199990000 |

## pfib — parallel fib — 100 computed at once across cores  (N=28)

| lang | wall | startup | compute | vs fastest | pos | peak RSS | mem | checksum |
|------|------|---------|---------|-----------|-----|----------|-----|----------|
| brood | 2.333s | 29.4ms | 2.304s | 29.6× | 6/6 | 12.4 MB | 1/6 | 31781100 |
| elixir | 548.9ms | 326.2ms | 222.7ms | 7.0× | 3/6 | 81.2 MB | 5/6 | 31781100 |
| python | 884.7ms | 13.0ms | 871.7ms | 11.2× | 5/6 | 22.1 MB | 2/6 | 31781100 |
| node | 176.4ms | 21.3ms | 155.1ms | 2.2× | 2/6 | 185.3 MB | 6/6 | 31781100 |
| ruby | 623.2ms | 57.7ms | 565.5ms | 7.9× | 4/6 | 23.7 MB | 3/6 | 31781100 |
| dotnet | 78.9ms | 24.1ms | 54.8ms | 1.0× | 1/6 | 27.9 MB | 4/6 | 31781100 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | wall | startup | compute | vs fastest | pos | peak RSS | mem | checksum |
|------|------|---------|---------|-----------|-----|----------|-----|----------|
| brood | 177.7ms | 29.4ms | 148.3ms | 1.4× | 3/5 | 65.5 MB | 3/5 | 0 |
| elixir | 1.048s | 326.2ms | 722.0ms | 8.0× | 5/5 | 591.3 MB | 5/5 | 0 |
| python | — | — | — | — | — | — | — | ERROR |
| node | 132.0ms | 21.3ms | 110.7ms | 1.0× | 2/5 | 66.6 MB | 4/5 | 0 |
| ruby | 266.9ms | 57.7ms | 209.2ms | 2.0× | 4/5 | 50.3 MB | 2/5 | 0 |
| dotnet | 130.8ms | 24.1ms | 106.7ms | 1.0× | 1/5 | 47.9 MB | 1/5 | 0 |
