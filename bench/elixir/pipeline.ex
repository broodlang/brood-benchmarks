defmodule Bpipeline do
  def main do
    n = String.to_integer(System.get_env("BENCH_N") || "100000")

    sum =
      0..(n - 1)
      |> Stream.filter(fn i -> rem(i, 3) == 0 or rem(i, 5) == 0 end)
      |> Stream.map(fn i -> i * i end)
      |> Enum.reduce(0, &+/2)

    IO.puts(sum)
  end
end
