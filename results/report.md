# Brood vs Elixir vs Python vs Node — benchmark results

_Best of 3 runs per program; full sizes. Wall = total process time (startup + compute). RSS = peak resident memory._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 9.5ms | 1.0× | 8.7 MB | 0 |
| elixir | 309.3ms | 32.6× | 93.0 MB | 0 |
| python | 13.7ms | 1.4× | 9.5 MB | 0 |
| node | 22.2ms | 2.3× | 44.7 MB | 0 |

## fib — naive recursion / function-call overhead  (N=30)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 2.234s | 60.4× | 15.5 MB | 832040 |
| elixir | 356.1ms | 9.6× | 93.9 MB | 832040 |
| python | 73.8ms | 2.0× | 9.6 MB | 832040 |
| node | 37.0ms | 1.0× | 50.6 MB | 832040 |

## loop — raw iteration (tail recursion vs for-loop)  (N=3000000)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 3.463s | 146.1× | 15.6 MB | 3000000 |
| elixir | 365.7ms | 15.4× | 93.7 MB | 3000000 |
| python | 187.7ms | 7.9× | 9.5 MB | 3000000 |
| node | 23.7ms | 1.0× | 50.6 MB | 3000000 |

## reduce — higher-order fold over a range  (N=1000000)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 4.699s | 148.2× | 253.8 MB | 499999500000 |
| elixir | 305.5ms | 9.6× | 92.4 MB | 499999500000 |
| python | 51.1ms | 1.6× | 10.2 MB | 499999500000 |
| node | 31.7ms | 1.0× | 52.7 MB | 499999500000 |

## primes — integer arithmetic (trial division)  (N=20000)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 457.8ms | 18.9× | 15.5 MB | 2262 |
| elixir | 358.3ms | 14.8× | 94.9 MB | 2262 |
| python | 24.2ms | 1.0× | 9.6 MB | 2262 |
| node | 27.3ms | 1.1× | 50.8 MB | 2262 |

## collatz — integer arithmetic + tight inner loop  (N=30000)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 5.455s | 144.7× | 15.7 MB | 307 |
| elixir | 365.3ms | 9.7× | 94.7 MB | 307 |
| python | 230.9ms | 6.1× | 9.3 MB | 307 |
| node | 37.7ms | 1.0× | 50.6 MB | 307 |

## mandelbrot — floating-point math (escape iterations)  (N=128)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 1.587s | 65.9× | 16.4 MB | 345426 |
| elixir | 370.9ms | 15.4× | 94.2 MB | 345426 |
| python | 77.7ms | 3.2× | 9.8 MB | 345426 |
| node | 24.1ms | 1.0× | 51.7 MB | 345426 |

## matmul — nested loops + indexing (integer NxN)  (N=80)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 3.383s | 140.4× | 19.2 MB | 229499993 |
| elixir | 327.7ms | 13.6× | 94.6 MB | 229499993 |
| python | 56.7ms | 2.4× | 9.8 MB | 229499993 |
| node | 24.1ms | 1.0× | 51.4 MB | 229499993 |

## strings — string building (join) + length  (N=50000)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 564.2ms | 33.0× | 65.6 MB | 288889 |
| elixir | 338.3ms | 19.8× | 100.8 MB | 288889 |
| python | 17.1ms | 1.0× | 12.6 MB | 288889 |
| node | 26.8ms | 1.6× | 55.4 MB | 288889 |

## wordcount — hash-map build (immutable vs mutable)  (N=100000)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 610.1ms | 19.1× | 22.1 MB | 50038280 |
| elixir | 354.1ms | 11.1× | 91.9 MB | 50038280 |
| python | 32.2ms | 1.0× | 9.8 MB | 50038280 |
| node | 32.0ms | 1.0× | 53.2 MB | 50038280 |

## bintree — allocation / GC pressure (build+walk trees)  (N=40)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 1.395s | 53.0× | 22.4 MB | 327640 |
| elixir | 360.3ms | 13.7× | 96.7 MB | 327640 |
| python | 29.0ms | 1.1× | 9.8 MB | 327640 |
| node | 26.3ms | 1.0× | 54.4 MB | 327640 |

## sort — sort a list of ints + checksum walk  (N=50000)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 207.3ms | 7.2× | 20.6 MB | 102632633 |
| elixir | 324.2ms | 11.2× | 101.1 MB | 102632633 |
| python | 28.9ms | 1.0× | 11.7 MB | 102632633 |
| node | 37.2ms | 1.3× | 53.8 MB | 102632633 |

## spawn — lightweight processes + messaging  (N=20000)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 638.7ms | 1.8× | 29.6 MB | 199990000 |
| elixir | 346.5ms | 1.0× | 111.0 MB | 199990000 |
