# Fan out N lightweight processes, each sends its index back; parent sums them.
# Checksum = sum(0..N-1) = N*(N-1)/2.
n = String.to_integer(System.get_env("BENCH_N") || "20000")
parent = self()

Enum.each(0..(n - 1), fn i -> spawn(fn -> send(parent, {:done, i}) end) end)

total = Enum.reduce(1..n, 0, fn _, acc -> receive do {:done, i} -> acc + i end end)
IO.puts(total)
