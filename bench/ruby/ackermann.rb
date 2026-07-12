# Ackermann ack(3,9) summed N times. Deep double-recursion (depth ~4093).
# Checksum = N * ack(3,9) = N * 4093.
n = (ENV["BENCH_N"] || "6").to_i

def ack(m, k)
  return k + 1 if m == 0
  return ack(m - 1, 1) if k == 0
  ack(m - 1, ack(m, k - 1))
end

total = 0
n.times { total += ack(3, 9) }
puts total
