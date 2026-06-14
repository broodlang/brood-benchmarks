n = (ENV["BENCH_N"] || "200000").to_i

# map / filter / reduce pipeline: square the multiples of 3 or 5, sum the squares.
total = (0...n).select { |i| i % 3 == 0 || i % 5 == 0 }.map { |i| i * i }.reduce(0, :+)
puts total
