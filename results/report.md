# Brood vs Elixir vs Python vs Node vs Ruby — benchmark results

_Best of 3 runs per program; full sizes. Wall = total process time (startup + compute). RSS = peak resident memory. `pos` = rank by wall, `mem` = rank by RSS (1 = best), out of the languages with a port._
> _`startup` and `http` are latency-sensitive; measured in isolation (best of 5) so neighbouring benchmarks' load doesn't inflate them. All other rows are best of 3 from the full suite._


## startup — interpreter/VM startup + base memory  (N=0)

| lang | wall | vs fastest | pos | peak RSS | mem | checksum |
|------|------|-----------|-----|----------|-----|----------|
| brood | 24.3ms | 1.7× | 3/5 | 10.6 MB | 2/5 | 0 |
| elixir | 327.1ms | 22.3× | 5/5 | 90.9 MB | 5/5 | 0 |
| python | 14.7ms | 1.0× | 1/5 | 9.4 MB | 1/5 | 0 |
| node | 23.5ms | 1.6× | 2/5 | 44.7 MB | 4/5 | 0 |
| ruby | 42.7ms | 2.9× | 4/5 | 23.2 MB | 3/5 | 0 |

## fib — naive recursion / function-call overhead  (N=30)

| lang | wall | vs fastest | pos | peak RSS | mem | checksum |
|------|------|-----------|-----|----------|-----|----------|
| brood | 365.3ms | 12.0× | 4/5 | 10.4 MB | 2/5 | 832040 |
| elixir | 372.5ms | 12.3× | 5/5 | 98.3 MB | 5/5 | 832040 |
| python | 72.5ms | 2.4× | 2/5 | 9.5 MB | 1/5 | 832040 |
| node | 30.4ms | 1.0× | 1/5 | 50.9 MB | 4/5 | 832040 |
| ruby | 100.3ms | 3.3× | 3/5 | 23.0 MB | 3/5 | 832040 |

## loop — raw iteration (tail recursion vs for-loop)  (N=3000000)

| lang | wall | vs fastest | pos | peak RSS | mem | checksum |
|------|------|-----------|-----|----------|-----|----------|
| brood | 430.7ms | 17.5× | 5/5 | 10.9 MB | 2/5 | 3000000 |
| elixir | 369.4ms | 15.0× | 4/5 | 95.4 MB | 5/5 | 3000000 |
| python | 190.3ms | 7.7× | 3/5 | 9.5 MB | 1/5 | 3000000 |
| node | 24.6ms | 1.0× | 1/5 | 50.6 MB | 4/5 | 3000000 |
| ruby | 109.0ms | 4.4× | 2/5 | 22.9 MB | 3/5 | 3000000 |

## reduce — higher-order fold over a range  (N=1000000)

| lang | wall | vs fastest | pos | peak RSS | mem | checksum |
|------|------|-----------|-----|----------|-----|----------|
| brood | 1.394s | 77.0× | 5/5 | 130.1 MB | 5/5 | 499999500000 |
| elixir | 345.8ms | 19.1× | 4/5 | 90.7 MB | 4/5 | 499999500000 |
| python | 18.1ms | 1.0× | 1/5 | 9.3 MB | 1/5 | 499999500000 |
| node | 27.3ms | 1.5× | 2/5 | 52.6 MB | 3/5 | 499999500000 |
| ruby | 44.4ms | 2.5× | 3/5 | 23.1 MB | 2/5 | 499999500000 |

## primes — integer arithmetic (trial division)  (N=20000)

| lang | wall | vs fastest | pos | peak RSS | mem | checksum |
|------|------|-----------|-----|----------|-----|----------|
| brood | 90.6ms | 4.1× | 4/5 | 10.7 MB | 2/5 | 2262 |
| elixir | 386.5ms | 17.6× | 5/5 | 94.6 MB | 5/5 | 2262 |
| python | 21.9ms | 1.0× | 1/5 | 9.5 MB | 1/5 | 2262 |
| node | 32.8ms | 1.5× | 2/5 | 50.9 MB | 4/5 | 2262 |
| ruby | 52.3ms | 2.4× | 3/5 | 23.3 MB | 3/5 | 2262 |

## collatz — integer arithmetic + tight inner loop  (N=30000)

| lang | wall | vs fastest | pos | peak RSS | mem | checksum |
|------|------|-----------|-----|----------|-----|----------|
| brood | 1.097s | 35.6× | 5/5 | 18.3 MB | 2/5 | 307 |
| elixir | 369.1ms | 12.0× | 4/5 | 97.3 MB | 5/5 | 307 |
| python | 232.3ms | 7.5× | 3/5 | 9.5 MB | 1/5 | 307 |
| node | 30.8ms | 1.0× | 1/5 | 50.6 MB | 4/5 | 307 |
| ruby | 134.2ms | 4.4× | 2/5 | 22.9 MB | 3/5 | 307 |

## mandelbrot — floating-point math (escape iterations)  (N=128)

| lang | wall | vs fastest | pos | peak RSS | mem | checksum |
|------|------|-----------|-----|----------|-----|----------|
| brood | 352.5ms | 13.6× | 4/5 | 10.6 MB | 2/5 | 345426 |
| elixir | 366.1ms | 14.1× | 5/5 | 96.8 MB | 5/5 | 345426 |
| python | 76.8ms | 3.0× | 3/5 | 10.0 MB | 1/5 | 345426 |
| node | 26.0ms | 1.0× | 1/5 | 51.7 MB | 4/5 | 345426 |
| ruby | 69.7ms | 2.7× | 2/5 | 23.4 MB | 3/5 | 345426 |

## matmul — nested loops + indexing (integer NxN)  (N=80)

| lang | wall | vs fastest | pos | peak RSS | mem | checksum |
|------|------|-----------|-----|----------|-----|----------|
| brood | 784.9ms | 28.4× | 5/5 | 19.2 MB | 2/5 | 229499993 |
| elixir | 335.4ms | 12.2× | 4/5 | 93.1 MB | 5/5 | 229499993 |
| python | 56.9ms | 2.1× | 2/5 | 9.8 MB | 1/5 | 229499993 |
| node | 27.6ms | 1.0× | 1/5 | 51.5 MB | 4/5 | 229499993 |
| ruby | 66.3ms | 2.4× | 3/5 | 23.1 MB | 3/5 | 229499993 |

## strings — string building (join) + length  (N=50000)

| lang | wall | vs fastest | pos | peak RSS | mem | checksum |
|------|------|-----------|-----|----------|-----|----------|
| brood | 218.2ms | 9.7× | 4/5 | 34.8 MB | 3/5 | 288889 |
| elixir | 331.9ms | 14.8× | 5/5 | 102.6 MB | 5/5 | 288889 |
| python | 22.5ms | 1.0× | 1/5 | 12.7 MB | 1/5 | 288889 |
| node | 33.5ms | 1.5× | 2/5 | 55.1 MB | 4/5 | 288889 |
| ruby | 53.7ms | 2.4× | 3/5 | 25.6 MB | 2/5 | 288889 |

## wordcount — hash-map build (immutable vs mutable)  (N=100000)

| lang | wall | vs fastest | pos | peak RSS | mem | checksum |
|------|------|-----------|-----|----------|-----|----------|
| brood | 613.9ms | 21.5× | 5/5 | 28.8 MB | 3/5 | 50038280 |
| elixir | 318.1ms | 11.1× | 4/5 | 93.3 MB | 5/5 | 50038280 |
| python | 28.8ms | 1.0× | 2/5 | 9.9 MB | 1/5 | 50038280 |
| node | 28.6ms | 1.0× | 1/5 | 53.1 MB | 4/5 | 50038280 |
| ruby | 51.2ms | 1.8× | 3/5 | 23.3 MB | 2/5 | 50038280 |

## bintree — allocation / GC pressure (build+walk trees)  (N=40)

| lang | wall | vs fastest | pos | peak RSS | mem | checksum |
|------|------|-----------|-----|----------|-----|----------|
| brood | 466.2ms | 17.2× | 5/5 | 14.5 MB | 2/5 | 327640 |
| elixir | 340.5ms | 12.6× | 4/5 | 94.9 MB | 5/5 | 327640 |
| python | 29.3ms | 1.1× | 2/5 | 10.0 MB | 1/5 | 327640 |
| node | 27.1ms | 1.0× | 1/5 | 54.8 MB | 4/5 | 327640 |
| ruby | 61.3ms | 2.3× | 3/5 | 23.2 MB | 3/5 | 327640 |

## sort — sort a list of ints + checksum walk  (N=50000)

| lang | wall | vs fastest | pos | peak RSS | mem | checksum |
|------|------|-----------|-----|----------|-----|----------|
| brood | 123.8ms | 4.3× | 4/5 | 19.9 MB | 2/5 | 102632633 |
| elixir | 342.5ms | 12.0× | 5/5 | 100.1 MB | 5/5 | 102632633 |
| python | 28.5ms | 1.0× | 1/5 | 12.0 MB | 1/5 | 102632633 |
| node | 42.3ms | 1.5× | 2/5 | 53.7 MB | 4/5 | 102632633 |
| ruby | 51.6ms | 1.8× | 3/5 | 23.6 MB | 3/5 | 102632633 |

## spawn — lightweight processes + messaging  (N=20000)

| lang | wall | vs fastest | pos | peak RSS | mem | checksum |
|------|------|-----------|-----|----------|-----|----------|
| brood | 631.9ms | 1.6× | 2/2 | 36.8 MB | 1/2 | 199990000 |
| elixir | 388.5ms | 1.0× | 1/2 | 113.5 MB | 2/2 | 199990000 |

## pfib — parallel fib — 100 computed at once across cores  (N=28)

| lang | wall | vs fastest | pos | peak RSS | mem | checksum |
|------|------|-----------|-----|----------|-----|----------|
| brood | 816.7ms | 6.0× | 5/5 | 26.0 MB | 3/5 | 31781100 |
| elixir | 377.5ms | 2.8× | 4/5 | 99.4 MB | 4/5 | 31781100 |
| python | 305.4ms | 2.3× | 3/5 | 22.2 MB | 1/5 | 31781100 |
| node | 135.2ms | 1.0× | 1/5 | 333.8 MB | 5/5 | 31781100 |
| ruby | 178.1ms | 1.3× | 2/5 | 23.4 MB | 2/5 | 31781100 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | wall | vs fastest | pos | peak RSS | mem | checksum |
|------|------|-----------|-----|----------|-----|----------|
| brood | 238.1ms | 1.2× | 3/5 | 50.3 MB | 3/5 | 500 |
| elixir | 640.9ms | 3.2× | 5/5 | 778.7 MB | 5/5 | 500 |
| python | 226.8ms | 1.1× | 2/5 | 46.3 MB | 1/5 | 500 |
| node | 201.0ms | 1.0× | 1/5 | 69.6 MB | 4/5 | 500 |
| ruby | 422.4ms | 2.1× | 4/5 | 49.9 MB | 2/5 | 500 |
