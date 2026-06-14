n = (ENV["BENCH_N"] || "750000").to_i
k = 1000

x = 123456789
counts = Hash.new(0)
n.times do
  x = (x * 1103515245 + 12345) & 0x7FFFFFFF
  counts[x % k] += 1
end

total = 0
counts.each { |key, v| total += key * v }

puts total
