# Brood vs Elixir vs Python vs Node vs Ruby — benchmark results

_Best of 3 runs per program; full sizes. Wall = total process time (startup + compute). RSS = peak resident memory. `pos` = rank by wall, `mem` = rank by RSS (1 = best), out of the languages with a port._
> _`startup` and `http` are latency-sensitive; measured in isolation (best of 5) so neighbouring benchmarks' load doesn't inflate them. All other rows are best of 3 from the full suite._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | wall | vs fastest | pos | peak RSS | mem | checksum |
|------|------|-----------|-----|----------|-----|----------|
| brood | 27.3ms | 2.3× | 3/5 | 11.4 MB | 2/5 | 0 |
| elixir | 324.7ms | 27.1× | 5/5 | 91.4 MB | 5/5 | 0 |
| python | 12.0ms | 1.0× | 1/5 | 9.6 MB | 1/5 | 0 |
| node | 24.0ms | 2.0× | 2/5 | 44.7 MB | 4/5 | 0 |
| ruby | 43.0ms | 3.6× | 4/5 | 23.2 MB | 3/5 | 0 |

## fib — naive recursion / function-call overhead  (N=30)

| lang | wall | vs fastest | pos | peak RSS | mem | checksum |
|------|------|-----------|-----|----------|-----|----------|
| brood | 502.5ms | 17.4× | 5/5 | 11.5 MB | 2/5 | 832040 |
| elixir | 374.8ms | 13.0× | 4/5 | 98.1 MB | 5/5 | 832040 |
| python | 72.8ms | 2.5× | 2/5 | 9.4 MB | 1/5 | 832040 |
| node | 28.8ms | 1.0× | 1/5 | 50.3 MB | 4/5 | 832040 |
| ruby | 106.3ms | 3.7× | 3/5 | 23.1 MB | 3/5 | 832040 |

## loop — raw iteration (tail recursion vs for-loop)  (N=3000000)

| lang | wall | vs fastest | pos | peak RSS | mem | checksum |
|------|------|-----------|-----|----------|-----|----------|
| brood | 544.7ms | 18.4× | 5/5 | 11.4 MB | 2/5 | 3000000 |
| elixir | 362.6ms | 12.2× | 4/5 | 95.4 MB | 5/5 | 3000000 |
| python | 190.9ms | 6.4× | 3/5 | 9.5 MB | 1/5 | 3000000 |
| node | 29.6ms | 1.0× | 1/5 | 50.7 MB | 4/5 | 3000000 |
| ruby | 109.9ms | 3.7× | 2/5 | 23.2 MB | 3/5 | 3000000 |

## reduce — higher-order fold over a range  (N=1000000)

| lang | wall | vs fastest | pos | peak RSS | mem | checksum |
|------|------|-----------|-----|----------|-----|----------|
| brood | 269.2ms | 12.1× | 4/5 | 20.1 MB | 2/5 | 499999500000 |
| elixir | 329.7ms | 14.9× | 5/5 | 91.3 MB | 5/5 | 499999500000 |
| python | 22.2ms | 1.0× | 1/5 | 9.3 MB | 1/5 | 499999500000 |
| node | 23.8ms | 1.1× | 2/5 | 52.6 MB | 4/5 | 499999500000 |
| ruby | 44.2ms | 2.0× | 3/5 | 23.2 MB | 3/5 | 499999500000 |

## primes — integer arithmetic (trial division)  (N=20000)

| lang | wall | vs fastest | pos | peak RSS | mem | checksum |
|------|------|-----------|-----|----------|-----|----------|
| brood | 98.2ms | 4.4× | 4/5 | 11.5 MB | 2/5 | 2262 |
| elixir | 385.7ms | 17.4× | 5/5 | 94.7 MB | 5/5 | 2262 |
| python | 22.2ms | 1.0× | 1/5 | 9.5 MB | 1/5 | 2262 |
| node | 24.8ms | 1.1× | 2/5 | 51.0 MB | 4/5 | 2262 |
| ruby | 58.5ms | 2.6× | 3/5 | 23.2 MB | 3/5 | 2262 |

## collatz — integer arithmetic + tight inner loop  (N=30000)

| lang | wall | vs fastest | pos | peak RSS | mem | checksum |
|------|------|-----------|-----|----------|-----|----------|
| brood | 876.5ms | 28.1× | 5/5 | 19.0 MB | 2/5 | 307 |
| elixir | 390.1ms | 12.5× | 4/5 | 98.2 MB | 5/5 | 307 |
| python | 239.4ms | 7.7× | 3/5 | 9.6 MB | 1/5 | 307 |
| node | 31.2ms | 1.0× | 1/5 | 50.4 MB | 4/5 | 307 |
| ruby | 135.3ms | 4.3× | 2/5 | 23.2 MB | 3/5 | 307 |

## mandelbrot — floating-point math (escape iterations)  (N=128)

| lang | wall | vs fastest | pos | peak RSS | mem | checksum |
|------|------|-----------|-----|----------|-----|----------|
| brood | 394.2ms | 11.7× | 5/5 | 11.1 MB | 2/5 | 345426 |
| elixir | 364.5ms | 10.8× | 4/5 | 96.1 MB | 5/5 | 345426 |
| python | 77.5ms | 2.3× | 3/5 | 9.8 MB | 1/5 | 345426 |
| node | 33.7ms | 1.0× | 1/5 | 51.4 MB | 4/5 | 345426 |
| ruby | 69.9ms | 2.1× | 2/5 | 23.2 MB | 3/5 | 345426 |

## matmul — nested loops + indexing (integer NxN)  (N=80)

| lang | wall | vs fastest | pos | peak RSS | mem | checksum |
|------|------|-----------|-----|----------|-----|----------|
| brood | 886.2ms | 27.5× | 5/5 | 18.9 MB | 2/5 | 229499993 |
| elixir | 343.4ms | 10.7× | 4/5 | 91.4 MB | 5/5 | 229499993 |
| python | 64.1ms | 2.0× | 2/5 | 9.7 MB | 1/5 | 229499993 |
| node | 32.2ms | 1.0× | 1/5 | 51.6 MB | 4/5 | 229499993 |
| ruby | 94.7ms | 2.9× | 3/5 | 23.7 MB | 3/5 | 229499993 |

## strings — string building (join) + length  (N=50000)

| lang | wall | vs fastest | pos | peak RSS | mem | checksum |
|------|------|-----------|-----|----------|-----|----------|
| brood | 348.3ms | 12.6× | 4/5 | 36.4 MB | 3/5 | 288889 |
| elixir | 631.1ms | 22.9× | 5/5 | 99.3 MB | 5/5 | 288889 |
| python | 27.6ms | 1.0× | 1/5 | 12.8 MB | 1/5 | 288889 |
| node | 38.8ms | 1.4× | 2/5 | 55.2 MB | 4/5 | 288889 |
| ruby | 82.9ms | 3.0× | 3/5 | 25.7 MB | 2/5 | 288889 |

## wordcount — hash-map build (immutable vs mutable)  (N=100000)

| lang | wall | vs fastest | pos | peak RSS | mem | checksum |
|------|------|-----------|-----|----------|-----|----------|
| brood | 864.1ms | 29.8× | 5/5 | 28.5 MB | 3/5 | 50038280 |
| elixir | 333.1ms | 11.5× | 4/5 | 90.6 MB | 5/5 | 50038280 |
| python | 34.2ms | 1.2× | 2/5 | 9.4 MB | 1/5 | 50038280 |
| node | 29.0ms | 1.0× | 1/5 | 53.0 MB | 4/5 | 50038280 |
| ruby | 54.7ms | 1.9× | 3/5 | 23.0 MB | 2/5 | 50038280 |

## bintree — allocation / GC pressure (build+walk trees)  (N=40)

| lang | wall | vs fastest | pos | peak RSS | mem | checksum |
|------|------|-----------|-----|----------|-----|----------|
| brood | 580.4ms | 20.0× | 5/5 | 15.3 MB | 2/5 | 327640 |
| elixir | 364.2ms | 12.6× | 4/5 | 94.6 MB | 5/5 | 327640 |
| python | 30.2ms | 1.0× | 2/5 | 10.0 MB | 1/5 | 327640 |
| node | 29.0ms | 1.0× | 1/5 | 52.5 MB | 4/5 | 327640 |
| ruby | 61.2ms | 2.1× | 3/5 | 23.6 MB | 3/5 | 327640 |

## sort — sort a list of ints + checksum walk  (N=50000)

| lang | wall | vs fastest | pos | peak RSS | mem | checksum |
|------|------|-----------|-----|----------|-----|----------|
| brood | 140.3ms | 3.9× | 4/5 | 20.4 MB | 2/5 | 102632633 |
| elixir | 328.8ms | 9.1× | 5/5 | 99.9 MB | 5/5 | 102632633 |
| python | 36.2ms | 1.0× | 1/5 | 11.8 MB | 1/5 | 102632633 |
| node | 37.1ms | 1.0× | 2/5 | 53.2 MB | 4/5 | 102632633 |
| ruby | 53.2ms | 1.5× | 3/5 | 23.9 MB | 3/5 | 102632633 |

## spawn — lightweight processes + messaging  (N=20000)

| lang | wall | vs fastest | pos | peak RSS | mem | checksum |
|------|------|-----------|-----|----------|-----|----------|
| brood | 333.7ms | 1.0× | 1/2 | 38.1 MB | 1/2 | 199990000 |
| elixir | 367.0ms | 1.1× | 2/2 | 111.3 MB | 2/2 | 199990000 |

## pfib — parallel fib — 100 computed at once across cores  (N=28)

| lang | wall | vs fastest | pos | peak RSS | mem | checksum |
|------|------|-----------|-----|----------|-----|----------|
| brood | 1.028s | 5.2× | 5/5 | 28.4 MB | 3/5 | 31781100 |
| elixir | 568.5ms | 2.9× | 4/5 | 94.9 MB | 4/5 | 31781100 |
| python | 376.5ms | 1.9× | 3/5 | 21.6 MB | 1/5 | 31781100 |
| node | 197.1ms | 1.0× | 1/5 | 346.5 MB | 5/5 | 31781100 |
| ruby | 279.3ms | 1.4× | 2/5 | 23.8 MB | 2/5 | 31781100 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | wall | vs fastest | pos | peak RSS | mem | checksum |
|------|------|-----------|-----|----------|-----|----------|
| brood | 241.6ms | 1.3× | 2/5 | 84.2 MB | 4/5 | 500 |
| elixir | 643.0ms | 3.4× | 5/5 | 743.6 MB | 5/5 | 500 |
| python | 306.1ms | 1.6× | 3/5 | 52.4 MB | 2/5 | 500 |
| node | 190.7ms | 1.0× | 1/5 | 69.3 MB | 3/5 | 500 |
| ruby | 430.7ms | 2.3× | 4/5 | 50.3 MB | 1/5 | 500 |
