# Fan out N threads, each returning its index; join and sum.
# Thread is Ruby's lightest concurrent unit. The GVL prevents CPU parallelism
# but threads still give correct concurrent semantics and test thread
# creation/join overhead. Checksum = N*(N-1)/2.
n = (ENV["BENCH_N"] || "20000").to_i

threads = Array.new(n) { |i| Thread.new { i } }
puts threads.sum(&:value)
