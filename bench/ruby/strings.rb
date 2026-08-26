n = (ENV["BENCH_N"] || "500000").to_i
s = (0...n).to_a.join(",")
puts s.length
