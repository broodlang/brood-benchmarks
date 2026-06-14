# Parallel fib: compute fib(N) in 100 tasks at once, summed. Ruby's GVL means
# threads give no CPU speedup, so the idiomatic way to use cores is forking
# worker processes (like Python's multiprocessing). A pool sized to the core
# count splits the 100 tasks; each child computes its share and pipes back a
# subtotal. Checksum = 100*fib(N).
require "etc"

n = (ENV["BENCH_N"] || "30").to_i
tasks = 100

def fib(n)
  n < 2 ? n : fib(n - 1) + fib(n - 2)
end

workers = [tasks, Etc.nprocessors].min
readers = []

workers.times do |w|
  # strided assignment: how many of the `tasks` fibs this worker owns
  count = 0
  i = w
  while i < tasks
    count += 1
    i += workers
  end

  r, wio = IO.pipe
  fork do
    r.close
    sub = 0
    count.times { sub += fib(n) }
    wio.write(sub.to_s)
    wio.close
  end
  wio.close
  readers << r
end

total = 0
readers.each do |r|
  total += r.read.to_i
  r.close
end
Process.waitall

puts total
