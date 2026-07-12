# Two threads bounce a token N round trips via queues. Checksum = N.
n = (ENV["BENCH_N"] || "100000").to_i
q_to = Queue.new
q_from = Queue.new
t = Thread.new do
  loop do
    m = q_to.pop
    break if m < 0
    q_from.push(m)
  end
end
k = 0
while k < n
  q_to.push(k)
  q_from.pop
  k += 1
end
q_to.push(-1)
t.join
puts k
