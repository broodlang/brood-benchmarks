n = (ENV["BENCH_N"] || "5000000").to_i

# higher-order fold: + applied per element via a block. NOT (0...n).sum, which
# Ruby evaluates with the Gauss closed form (O(1)) and so does no folding work.
puts (0...n).reduce(0) { |a, b| a + b }
