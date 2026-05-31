n = (ENV["BENCH_N"] || "1000000").to_i

# idiomatic fast fold for addition over a range
puts (0...n).sum
