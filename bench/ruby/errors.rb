n = (ENV["BENCH_N"] || "200000").to_i
md = 1000000007

class BenchError < StandardError
  attr_reader :v
  def initialize(v); @v = v; end
end

acc = 0
(0...n).each do |i|
  begin
    raise BenchError.new(i % 100)
  rescue BenchError => e
    acc += e.v
  end
end

puts acc % md
