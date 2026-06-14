n = (ENV["BENCH_N"] || "30000000").to_i

acc = 0
i = 0
while i < n
  acc += i
  i += 1
end

puts acc
