n = String.to_integer(System.get_env("BENCH_N") || "50000")
s = Enum.join(0..(n - 1), ",")
IO.puts(String.length(s))
