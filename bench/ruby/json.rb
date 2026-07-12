# Build N records, JSON.generate then JSON.parse, checksum sum of "v" mod 2^31.
require "json"
n = (ENV["BENCH_N"] || "2000").to_i
x = 123456789
arr = []
n.times do |i|
  x = (x * 1103515245 + 12345) & 0x7FFFFFFF
  arr << { "id" => i, "v" => x, "name" => "item", "ok" => x.even? }
end
parsed = JSON.parse(JSON.generate(arr))
acc = 0
parsed.each { |o| acc = (acc + o["v"]) % 2147483647 }
puts acc
