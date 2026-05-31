n = (ENV["BENCH_N"] || "30000").to_i

best = 0
(1...n).each do |start|
  m = start
  steps = 0
  while m != 1
    m = m.even? ? m / 2 : 3 * m + 1
    steps += 1
  end
  best = steps if steps > best
end

puts best
