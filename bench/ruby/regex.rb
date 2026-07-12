# Generate N decimal strings; count full matches of \A[0-9]+\z. Checksum = count.
n = (ENV["BENCH_N"] || "20000").to_i
re = /\A[0-9]+\z/
x = 123456789
count = 0
n.times do
  x = (x * 1103515245 + 12345) & 0x7FFFFFFF
  s = x.to_s
  s += "x" if x.even?
  count += 1 if s.match?(re)
end
puts count
