n = (ENV["BENCH_N"] || "175").to_i
mod = 1000000007

a = Array.new(n) { |i| Array.new(n) { |j| (i + j) % 100 } }
b = Array.new(n) { |i| Array.new(n) { |j| (i * j) % 100 } }

total = 0
(0...n).each do |i|
  ai = a[i]
  (0...n).each do |j|
    s = 0
    (0...n).each { |k| s += ai[k] * b[k][j] }
    total += s
  end
end

puts total % mod
