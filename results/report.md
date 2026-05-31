# Brood vs Elixir vs Python vs Node — benchmark results

_Best of 3 runs per program; full sizes. Wall = total process time (startup + compute). RSS = peak resident memory._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 20.8ms | 1.7× | 10.6 MB | 0 |
| elixir | 326.4ms | 26.5× | 91.8 MB | 0 |
| python | 12.3ms | 1.0× | 9.6 MB | 0 |
| node | 22.9ms | 1.9× | 44.4 MB | 0 |

## fib — naive recursion / function-call overhead  (N=30)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 366.2ms | 11.9× | 10.9 MB | 832040 |
| elixir | 359.9ms | 11.7× | 97.0 MB | 832040 |
| python | 72.4ms | 2.4× | 9.5 MB | 832040 |
| node | 30.7ms | 1.0× | 50.6 MB | 832040 |

## loop — raw iteration (tail recursion vs for-loop)  (N=3000000)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 425.7ms | 17.7× | 10.8 MB | 3000000 |
| elixir | 362.5ms | 15.1× | 95.7 MB | 3000000 |
| python | 189.3ms | 7.9× | 9.6 MB | 3000000 |
| node | 24.0ms | 1.0× | 50.9 MB | 3000000 |

## reduce — higher-order fold over a range  (N=1000000)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 1.456s | 83.7× | 139.4 MB | 499999500000 |
| elixir | 319.6ms | 18.4× | 91.5 MB | 499999500000 |
| python | 17.4ms | 1.0× | 9.4 MB | 499999500000 |
| node | 22.5ms | 1.3× | 52.6 MB | 499999500000 |

## primes — integer arithmetic (trial division)  (N=20000)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 87.5ms | 4.4× | 10.7 MB | 2262 |
| elixir | 341.0ms | 17.0× | 97.6 MB | 2262 |
| python | 20.1ms | 1.0× | 9.7 MB | 2262 |
| node | 24.0ms | 1.2× | 51.1 MB | 2262 |

## collatz — integer arithmetic + tight inner loop  (N=30000)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 1.091s | 34.9× | 18.3 MB | 307 |
| elixir | 356.5ms | 11.4× | 93.8 MB | 307 |
| python | 227.5ms | 7.3× | 9.6 MB | 307 |
| node | 31.3ms | 1.0× | 50.9 MB | 307 |

## mandelbrot — floating-point math (escape iterations)  (N=128)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 348.7ms | 15.5× | 10.7 MB | 345426 |
| elixir | 368.4ms | 16.4× | 95.3 MB | 345426 |
| python | 80.3ms | 3.6× | 10.0 MB | 345426 |
| node | 22.5ms | 1.0× | 51.7 MB | 345426 |

## matmul — nested loops + indexing (integer NxN)  (N=80)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 788.1ms | 32.4× | 18.9 MB | 229499993 |
| elixir | 308.0ms | 12.7× | 91.8 MB | 229499993 |
| python | 52.9ms | 2.2× | 9.8 MB | 229499993 |
| node | 24.3ms | 1.0× | 51.2 MB | 229499993 |

## strings — string building (join) + length  (N=50000)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 230.1ms | 15.1× | 33.2 MB | 288889 |
| elixir | 318.3ms | 20.9× | 100.7 MB | 288889 |
| python | 15.2ms | 1.0× | 12.8 MB | 288889 |
| node | 26.5ms | 1.7× | 55.3 MB | 288889 |

## wordcount — hash-map build (immutable vs mutable)  (N=100000)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 630.9ms | 21.8× | 29.2 MB | 50038280 |
| elixir | 340.0ms | 11.7× | 91.7 MB | 50038280 |
| python | 32.2ms | 1.1× | 9.8 MB | 50038280 |
| node | 29.0ms | 1.0× | 52.7 MB | 50038280 |

## bintree — allocation / GC pressure (build+walk trees)  (N=40)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 469.4ms | 17.1× | 14.3 MB | 327640 |
| elixir | 365.8ms | 13.3× | 95.7 MB | 327640 |
| python | 29.2ms | 1.1× | 10.0 MB | 327640 |
| node | 27.5ms | 1.0× | 54.5 MB | 327640 |

## sort — sort a list of ints + checksum walk  (N=50000)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 127.0ms | 4.2× | 20.1 MB | 102632633 |
| elixir | 318.9ms | 10.7× | 100.1 MB | 102632633 |
| python | 29.9ms | 1.0× | 12.0 MB | 102632633 |
| node | 39.8ms | 1.3× | 54.2 MB | 102632633 |

## spawn — lightweight processes + messaging  (N=20000)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 632.9ms | 1.8× | 37.2 MB | 199990000 |
| elixir | 358.8ms | 1.0× | 114.2 MB | 199990000 |

## pfib — parallel fib — 100 computed at once across cores  (N=28)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 4.581s | 35.2× | 882.0 MB | 31781100 |
| elixir | 386.7ms | 3.0× | 96.3 MB | 31781100 |
| python | 316.8ms | 2.4× | 21.7 MB | 31781100 |
| node | 130.3ms | 1.0× | 340.0 MB | 31781100 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 192.5ms | 1.1× | 57.0 MB | 500 |
| elixir | 662.4ms | 3.7× | 788.0 MB | 500 |
| python | 219.3ms | 1.2× | 49.9 MB | 500 |
| node | 179.0ms | 1.0× | 69.5 MB | 500 |
