n = (ENV["BENCH_N"] || "750000").to_i
mod = 1000000007

x = 123456789
data = Array.new(n) do
  x = (x * 1103515245 + 12345) & 0x7FFFFFFF
  x
end

data.sort!

h = 0
data.each { |v| h = (h * 31 + v) % mod }

puts h
