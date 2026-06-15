n = (ENV["BENCH_N"] || "50000").to_i
md = 1000000007
DEPTH = 50

class BenchError < StandardError
  attr_reader :v
  def initialize(v); @v = v; end
end

def descend(d, i)
  raise BenchError.new(i % 100) if d == 0
  1 + descend(d - 1, i)
end

acc = 0
(0...n).each do |i|
  begin
    descend(DEPTH, i)
  rescue BenchError => e
    acc += e.v
  end
end
puts acc % md
