# A ring of N threads; a token travels around +1/hop for LAPS laps (N*LAPS hops).
# Checksum = N*LAPS.
n = (ENV["BENCH_N"] || "200").to_i
laps = 5000
total = n * laps
inboxes = Array.new(n) { Queue.new }
done = Queue.new
n.times do |i|
  Thread.new do
    inbox = inboxes[i]
    nxt = inboxes[(i + 1) % n]
    loop do
      v = inbox.pop
      if v >= total
        done.push(v)
        break
      end
      nxt.push(v + 1)
    end
  end
end
inboxes[0].push(0)
puts done.pop
