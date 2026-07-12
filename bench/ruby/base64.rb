# Generate N bytes, base64 encode+decode. Checksum = (sum enc char codes + sum
# decoded bytes) mod 2^31.
require "base64"
n = (ENV["BENCH_N"] || "50000").to_i
x = 123456789
bytes = Array.new(n)
n.times do |i|
  x = (x * 1103515245 + 12345) & 0x7FFFFFFF
  bytes[i] = x % 256
end
enc = Base64.strict_encode64(bytes.pack("C*"))
dec = Base64.strict_decode64(enc)
enc_sum = 0
enc.each_byte { |c| enc_sum = (enc_sum + c) % 2147483647 }
dec_sum = 0
dec.each_byte { |c| dec_sum = (dec_sum + c) % 2147483647 }
puts((enc_sum + dec_sum) % 2147483647)
