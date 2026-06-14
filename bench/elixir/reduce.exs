n = String.to_integer(System.get_env("BENCH_N") || "10000000")
# higher-order fold: + applied per element (Enum.reduce with a passed fn, not Enum.sum).
IO.puts(Enum.reduce(0..(n - 1), 0, fn x, acc -> acc + x end))
