n = (ENV["BENCH_N"] || "500000").to_i

s = (0...n).map(&:to_s).join(",")
puts s.length
