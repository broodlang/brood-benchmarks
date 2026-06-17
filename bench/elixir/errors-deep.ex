defmodule BenchErrorDeep do
  defexception [:v, message: "bench error"]
end

defmodule Berrorsdeep do
  def descend(0, i), do: raise(BenchErrorDeep, v: rem(i, 100))
  def descend(d, i), do: 1 + descend(d - 1, i)

  def main do
    n = String.to_integer(System.get_env("BENCH_N") || "50000")
    md = 1000000007
    depth = 50

    acc =
      Enum.reduce(0..(n - 1), 0, fn i, acc ->
        try do
          descend(depth, i)
        rescue
          e in BenchErrorDeep -> acc + e.v
        end
      end)

    IO.puts(rem(acc, md))
  end
end
