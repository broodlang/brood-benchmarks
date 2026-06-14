# Concurrent HTTP: fire N GETs at a local server (each sleeps ~20ms server-side)
# and count the 200s. Ruby releases the GVL during blocking I/O, so a thread per
# request overlaps the waits fine — the idiomatic stdlib way to do concurrent
# HTTP. Checksum = N.
require "net/http"
require "uri"

n = (ENV["BENCH_N"] || "500").to_i
port = ENV["BENCH_HTTP_PORT"] || "8089"
uri = URI("http://127.0.0.1:#{port}/")

threads = (0...n).map do
  Thread.new do
    res = Net::HTTP.get_response(uri)
    res.code == "200" ? 1 : 0
  end
end

puts threads.sum(&:value)
