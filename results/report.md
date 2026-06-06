# Brood vs Elixir vs Python vs Node vs Ruby — benchmark results

_Best of 3 runs per program; full sizes. Wall = total process time (startup + compute). RSS = peak resident memory. `pos` = rank by wall, `mem` = rank by RSS (1 = best), out of the languages with a port._
> _`startup` and `http` are latency-sensitive; measured in isolation (best of 5) so neighbouring benchmarks' load doesn't inflate them. All other rows are best of 3 from the full suite._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | wall | vs fastest | pos | peak RSS | mem | checksum |
|------|------|-----------|-----|----------|-----|----------|
| brood | 24.6ms | 2.1× | 2/5 | 10.6 MB | 2/5 | 0 |
| elixir | 314.7ms | 26.7× | 5/5 | 91.8 MB | 5/5 | 0 |
| python | 11.8ms | 1.0× | 1/5 | 9.5 MB | 1/5 | 0 |
| node | 24.9ms | 2.1× | 3/5 | 44.7 MB | 4/5 | 0 |
| ruby | 42.6ms | 3.6× | 4/5 | 23.2 MB | 3/5 | 0 |

## fib — naive recursion / function-call overhead  (N=30)

| lang | wall | vs fastest | pos | peak RSS | mem | checksum |
|------|------|-----------|-----|----------|-----|----------|
| brood | 496.6ms | 17.4× | 5/5 | 10.6 MB | 2/5 | 832040 |
| elixir | 360.0ms | 12.6× | 4/5 | 95.2 MB | 5/5 | 832040 |
| python | 71.9ms | 2.5× | 2/5 | 9.4 MB | 1/5 | 832040 |
| node | 28.6ms | 1.0× | 1/5 | 50.3 MB | 4/5 | 832040 |
| ruby | 96.7ms | 3.4× | 3/5 | 23.2 MB | 3/5 | 832040 |

## loop — raw iteration (tail recursion vs for-loop)  (N=3000000)

| lang | wall | vs fastest | pos | peak RSS | mem | checksum |
|------|------|-----------|-----|----------|-----|----------|
| brood | 541.5ms | 19.8× | 5/5 | 10.8 MB | 2/5 | 3000000 |
| elixir | 351.3ms | 12.9× | 4/5 | 94.9 MB | 5/5 | 3000000 |
| python | 185.6ms | 6.8× | 3/5 | 9.5 MB | 1/5 | 3000000 |
| node | 27.3ms | 1.0× | 1/5 | 50.4 MB | 4/5 | 3000000 |
| ruby | 120.7ms | 4.4× | 2/5 | 23.1 MB | 3/5 | 3000000 |

## reduce — higher-order fold over a range  (N=1000000)

| lang | wall | vs fastest | pos | peak RSS | mem | checksum |
|------|------|-----------|-----|----------|-----|----------|
| brood | 1.575s | 90.0× | 5/5 | 130.0 MB | 5/5 | 499999500000 |
| elixir | 321.0ms | 18.3× | 4/5 | 91.6 MB | 4/5 | 499999500000 |
| python | 17.5ms | 1.0× | 1/5 | 9.5 MB | 1/5 | 499999500000 |
| node | 26.8ms | 1.5× | 2/5 | 52.5 MB | 3/5 | 499999500000 |
| ruby | 43.5ms | 2.5× | 3/5 | 23.2 MB | 2/5 | 499999500000 |

## primes — integer arithmetic (trial division)  (N=20000)

| lang | wall | vs fastest | pos | peak RSS | mem | checksum |
|------|------|-----------|-----|----------|-----|----------|
| brood | 98.0ms | 4.8× | 4/5 | 10.6 MB | 2/5 | 2262 |
| elixir | 364.0ms | 17.7× | 5/5 | 94.6 MB | 5/5 | 2262 |
| python | 20.6ms | 1.0× | 1/5 | 9.8 MB | 1/5 | 2262 |
| node | 22.8ms | 1.1× | 2/5 | 51.2 MB | 4/5 | 2262 |
| ruby | 51.6ms | 2.5× | 3/5 | 23.2 MB | 3/5 | 2262 |

## collatz — integer arithmetic + tight inner loop  (N=30000)

| lang | wall | vs fastest | pos | peak RSS | mem | checksum |
|------|------|-----------|-----|----------|-----|----------|
| brood | 871.0ms | 27.6× | 5/5 | 18.2 MB | 2/5 | 307 |
| elixir | 355.3ms | 11.2× | 4/5 | 96.6 MB | 5/5 | 307 |
| python | 238.2ms | 7.5× | 3/5 | 9.8 MB | 1/5 | 307 |
| node | 31.6ms | 1.0× | 1/5 | 49.9 MB | 4/5 | 307 |
| ruby | 132.8ms | 4.2× | 2/5 | 23.2 MB | 3/5 | 307 |

## mandelbrot — floating-point math (escape iterations)  (N=128)

| lang | wall | vs fastest | pos | peak RSS | mem | checksum |
|------|------|-----------|-----|----------|-----|----------|
| brood | 382.2ms | 16.0× | 5/5 | 11.3 MB | 2/5 | 345426 |
| elixir | 366.8ms | 15.3× | 4/5 | 94.3 MB | 5/5 | 345426 |
| python | 79.2ms | 3.3× | 3/5 | 9.9 MB | 1/5 | 345426 |
| node | 23.9ms | 1.0× | 1/5 | 51.6 MB | 4/5 | 345426 |
| ruby | 76.1ms | 3.2× | 2/5 | 23.2 MB | 3/5 | 345426 |

## matmul — nested loops + indexing (integer NxN)  (N=80)

| lang | wall | vs fastest | pos | peak RSS | mem | checksum |
|------|------|-----------|-----|----------|-----|----------|
| brood | 911.8ms | 33.9× | 5/5 | 19.2 MB | 2/5 | 229499993 |
| elixir | 328.2ms | 12.2× | 4/5 | 92.4 MB | 5/5 | 229499993 |
| python | 55.0ms | 2.0× | 2/5 | 9.5 MB | 1/5 | 229499993 |
| node | 26.9ms | 1.0× | 1/5 | 51.0 MB | 4/5 | 229499993 |
| ruby | 66.2ms | 2.5× | 3/5 | 23.2 MB | 3/5 | 229499993 |

## strings — string building (join) + length  (N=50000)

| lang | wall | vs fastest | pos | peak RSS | mem | checksum |
|------|------|-----------|-----|----------|-----|----------|
| brood | 332.0ms | 20.9× | 5/5 | 39.2 MB | 3/5 | 288889 |
| elixir | 331.5ms | 20.8× | 4/5 | 100.8 MB | 5/5 | 288889 |
| python | 15.9ms | 1.0× | 1/5 | 12.7 MB | 1/5 | 288889 |
| node | 28.4ms | 1.8× | 2/5 | 55.3 MB | 4/5 | 288889 |
| ruby | 50.4ms | 3.2× | 3/5 | 25.6 MB | 2/5 | 288889 |

## wordcount — hash-map build (immutable vs mutable)  (N=100000)

| lang | wall | vs fastest | pos | peak RSS | mem | checksum |
|------|------|-----------|-----|----------|-----|----------|
| brood | 700.3ms | 22.4× | 5/5 | 30.0 MB | 3/5 | 50038280 |
| elixir | 359.3ms | 11.5× | 4/5 | 91.5 MB | 5/5 | 50038280 |
| python | 31.3ms | 1.0× | 1/5 | 9.6 MB | 1/5 | 50038280 |
| node | 32.1ms | 1.0× | 2/5 | 52.8 MB | 4/5 | 50038280 |
| ruby | 53.2ms | 1.7× | 3/5 | 23.2 MB | 2/5 | 50038280 |

## bintree — allocation / GC pressure (build+walk trees)  (N=40)

| lang | wall | vs fastest | pos | peak RSS | mem | checksum |
|------|------|-----------|-----|----------|-----|----------|
| brood | 569.2ms | 21.5× | 5/5 | 14.7 MB | 2/5 | 327640 |
| elixir | 350.2ms | 13.2× | 4/5 | 94.1 MB | 5/5 | 327640 |
| python | 29.5ms | 1.1× | 2/5 | 9.9 MB | 1/5 | 327640 |
| node | 26.5ms | 1.0× | 1/5 | 54.5 MB | 4/5 | 327640 |
| ruby | 62.4ms | 2.4× | 3/5 | 23.4 MB | 3/5 | 327640 |

## sort — sort a list of ints + checksum walk  (N=50000)

| lang | wall | vs fastest | pos | peak RSS | mem | checksum |
|------|------|-----------|-----|----------|-----|----------|
| brood | 140.8ms | 4.4× | 4/5 | 20.0 MB | 2/5 | 102632633 |
| elixir | 331.1ms | 10.4× | 5/5 | 103.8 MB | 5/5 | 102632633 |
| python | 31.9ms | 1.0× | 1/5 | 12.1 MB | 1/5 | 102632633 |
| node | 39.2ms | 1.2× | 2/5 | 53.7 MB | 4/5 | 102632633 |
| ruby | 51.4ms | 1.6× | 3/5 | 23.6 MB | 3/5 | 102632633 |

## spawn — lightweight processes + messaging  (N=20000)

| lang | wall | vs fastest | pos | peak RSS | mem | checksum |
|------|------|-----------|-----|----------|-----|----------|
| brood | 388.5ms | 1.1× | 2/2 | 37.7 MB | 1/2 | 199990000 |
| elixir | 360.1ms | 1.0× | 1/2 | 113.4 MB | 2/2 | 199990000 |

## pfib — parallel fib — 100 computed at once across cores  (N=28)

| lang | wall | vs fastest | pos | peak RSS | mem | checksum |
|------|------|-----------|-----|----------|-----|----------|
| brood | 1.103s | 7.3× | 5/5 | 26.8 MB | 3/5 | 31781100 |
| elixir | 431.8ms | 2.9× | 4/5 | 95.8 MB | 4/5 | 31781100 |
| python | 319.6ms | 2.1× | 3/5 | 21.4 MB | 1/5 | 31781100 |
| node | 150.8ms | 1.0× | 1/5 | 321.0 MB | 5/5 | 31781100 |
| ruby | 230.4ms | 1.5× | 2/5 | 23.5 MB | 2/5 | 31781100 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | wall | vs fastest | pos | peak RSS | mem | checksum |
|------|------|-----------|-----|----------|-----|----------|
| brood | 197.3ms | 1.0× | 2/5 | 79.8 MB | 4/5 | 500 |
| elixir | 686.8ms | 3.6× | 5/5 | 790.5 MB | 5/5 | 500 |
| python | 262.6ms | 1.4× | 3/5 | 50.5 MB | 2/5 | 500 |
| node | 188.6ms | 1.0× | 1/5 | 69.1 MB | 3/5 | 500 |
| ruby | 363.3ms | 1.9× | 4/5 | 49.9 MB | 1/5 | 500 |
