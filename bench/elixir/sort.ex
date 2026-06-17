defmodule Bsort do
  import Bitwise

  def main do
    n = String.to_integer(System.get_env("BENCH_N") || "375000")
    mod = 1_000_000_007

    {_, data} =
      Enum.reduce(1..n, {123_456_789, []}, fn _, {x, acc} ->
        x2 = band(x * 1_103_515_245 + 12_345, 0x7FFFFFFF)
        {x2, [x2 | acc]}
      end)

    sorted = Enum.sort(data)
    h = Enum.reduce(sorted, 0, fn v, h -> rem(h * 31 + v, mod) end)
    IO.puts(h)
  end
end
