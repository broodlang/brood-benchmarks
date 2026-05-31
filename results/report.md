# Brood vs Elixir vs Python vs Node — benchmark results

_Best of 3 runs per program; full sizes. Wall = total process time (startup + compute). RSS = peak resident memory._
> _`startup` and `http` are latency-sensitive; measured in isolation (best of 5) so neighbouring benchmarks' load doesn't inflate them. All other rows are best of 3 from the full suite._


## startup — interpreter/VM startup + base memory  (N=0)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 24.2ms | 2.2× | 10.7 MB | 0 |
| elixir | 321.8ms | 28.7× | 92.0 MB | 0 |
| python | 11.2ms | 1.0× | 9.6 MB | 0 |
| node | 21.0ms | 1.9× | 44.7 MB | 0 |

## fib — naive recursion / function-call overhead  (N=30)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 363.1ms | 12.6× | 10.6 MB | 832040 |
| elixir | 348.0ms | 12.0× | 97.4 MB | 832040 |
| python | 73.3ms | 2.5× | 9.4 MB | 832040 |
| node | 28.9ms | 1.0× | 50.4 MB | 832040 |

## loop — raw iteration (tail recursion vs for-loop)  (N=3000000)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 424.8ms | 15.1× | 10.9 MB | 3000000 |
| elixir | 352.6ms | 12.5× | 95.8 MB | 3000000 |
| python | 190.6ms | 6.8× | 9.5 MB | 3000000 |
| node | 28.2ms | 1.0× | 50.6 MB | 3000000 |

## reduce — higher-order fold over a range  (N=1000000)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 1.450s | 78.4× | 139.6 MB | 499999500000 |
| elixir | 328.5ms | 17.8× | 91.7 MB | 499999500000 |
| python | 18.5ms | 1.0× | 9.7 MB | 499999500000 |
| node | 26.3ms | 1.4× | 52.8 MB | 499999500000 |

## primes — integer arithmetic (trial division)  (N=20000)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 86.9ms | 4.5× | 10.7 MB | 2262 |
| elixir | 357.8ms | 18.4× | 96.8 MB | 2262 |
| python | 19.4ms | 1.0× | 9.7 MB | 2262 |
| node | 25.6ms | 1.3× | 51.2 MB | 2262 |

## collatz — integer arithmetic + tight inner loop  (N=30000)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 1.093s | 37.6× | 18.0 MB | 307 |
| elixir | 386.6ms | 13.3× | 95.0 MB | 307 |
| python | 233.0ms | 8.0× | 9.4 MB | 307 |
| node | 29.1ms | 1.0× | 50.5 MB | 307 |

## mandelbrot — floating-point math (escape iterations)  (N=128)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 350.5ms | 13.6× | 10.9 MB | 345426 |
| elixir | 372.6ms | 14.5× | 97.4 MB | 345426 |
| python | 76.2ms | 3.0× | 9.7 MB | 345426 |
| node | 25.7ms | 1.0× | 51.5 MB | 345426 |

## matmul — nested loops + indexing (integer NxN)  (N=80)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 788.1ms | 31.7× | 18.6 MB | 229499993 |
| elixir | 340.2ms | 13.7× | 91.9 MB | 229499993 |
| python | 54.5ms | 2.2× | 9.6 MB | 229499993 |
| node | 24.9ms | 1.0× | 51.3 MB | 229499993 |

## strings — string building (join) + length  (N=50000)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 232.6ms | 14.4× | 33.1 MB | 288889 |
| elixir | 343.3ms | 21.2× | 103.0 MB | 288889 |
| python | 16.2ms | 1.0× | 12.7 MB | 288889 |
| node | 28.1ms | 1.7× | 55.5 MB | 288889 |

## wordcount — hash-map build (immutable vs mutable)  (N=100000)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 616.7ms | 21.9× | 29.7 MB | 50038280 |
| elixir | 360.7ms | 12.8× | 94.9 MB | 50038280 |
| python | 30.0ms | 1.1× | 9.5 MB | 50038280 |
| node | 28.1ms | 1.0× | 53.6 MB | 50038280 |

## bintree — allocation / GC pressure (build+walk trees)  (N=40)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 466.4ms | 17.6× | 14.5 MB | 327640 |
| elixir | 357.9ms | 13.5× | 94.7 MB | 327640 |
| python | 28.3ms | 1.1× | 9.8 MB | 327640 |
| node | 26.5ms | 1.0× | 54.6 MB | 327640 |

## sort — sort a list of ints + checksum walk  (N=50000)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 123.3ms | 4.0× | 20.1 MB | 102632633 |
| elixir | 334.9ms | 10.8× | 100.4 MB | 102632633 |
| python | 30.9ms | 1.0× | 11.7 MB | 102632633 |
| node | 43.3ms | 1.4× | 53.7 MB | 102632633 |

## spawn — lightweight processes + messaging  (N=20000)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 620.5ms | 1.6× | 37.4 MB | 199990000 |
| elixir | 379.9ms | 1.0× | 113.7 MB | 199990000 |

## pfib — parallel fib — 100 computed at once across cores  (N=28)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 4.179s | 32.0× | 978.7 MB | 31781100 |
| elixir | 357.9ms | 2.7× | 95.7 MB | 31781100 |
| python | 298.5ms | 2.3× | 21.6 MB | 31781100 |
| node | 130.5ms | 1.0× | 306.6 MB | 31781100 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 200.2ms | 1.2× | 63.2 MB | 500 |
| elixir | 646.8ms | 3.8× | 802.5 MB | 500 |
| python | 312.0ms | 1.9× | 46.8 MB | 500 |
| node | 168.1ms | 1.0× | 69.2 MB | 500 |
