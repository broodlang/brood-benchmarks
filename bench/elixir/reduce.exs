n = String.to_integer(System.get_env("BENCH_N") || "1000000")
IO.puts(Enum.sum(0..(n - 1)))
