n = (ENV["BENCH_N"] || "3000000").to_i

acc = 0
i = 0
while i < n
  acc += 1
  i += 1
end

puts acc
