n = String.to_integer(System.get_env("BENCH_N") || "200000")
md = 1000000007

defmodule BenchError do
  defexception [:v, message: "bench error"]
end

acc =
  Enum.reduce(0..(n - 1), 0, fn i, acc ->
    try do
      raise BenchError, v: rem(i, 100)
    rescue
      e in BenchError -> acc + e.v
    end
  end)

IO.puts(rem(acc, md))
