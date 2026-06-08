# Fan out N threads; each computes fib(15) and returns the result.
# Tests thread fan-out under real CPU work per unit.
# Checksum = N * fib(15) = N * 610.
n = (ENV["BENCH_N"] || "20000").to_i

def fib(n)
  n < 2 ? n : fib(n - 1) + fib(n - 2)
end

threads = Array.new(n) { Thread.new { fib(15) } }
puts threads.sum(&:value)
