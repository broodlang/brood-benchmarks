n = (ENV["BENCH_N"] || "50000").to_i

s = (0...n).map(&:to_s).join(",")
puts s.length
