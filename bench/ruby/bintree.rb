n = (ENV["BENCH_N"] || "200").to_i   # repetitions
depth = 12

def make(d)
  return nil if d == 0
  [make(d - 1), make(d - 1)]
end

def check(node)
  return 1 if node.nil?
  1 + check(node[0]) + check(node[1])
end

total = 0
n.times { total += check(make(depth)) }

puts total
