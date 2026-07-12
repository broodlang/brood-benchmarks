# Read-modify-write churn on a Hash over a 50k key space.
# Checksum = sum of key*value over the map.
n = (ENV["BENCH_N"] || "300000").to_i
m = 50000
x = 123456789
h = Hash.new(0)
n.times do
  x = (x * 1103515245 + 12345) & 0x7FFFFFFF
  key = x % m
  h[key] += 1 + (key % 7)
end
total = 0
h.each { |k, v| total += k * v }
puts total
