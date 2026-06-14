n = (ENV["BENCH_N"] || "10").to_i

def safe?(c, placed, d)
  placed.each do |p|
    return false if p == c || p - c == d || p - c == -d
    d += 1
  end
  true
end

def solve(row, n, placed)
  return 1 if row == n
  total = 0
  (0...n).each do |c|
    total += solve(row + 1, n, [c] + placed) if safe?(c, placed, 1)
  end
  total
end

puts solve(0, n, [])
