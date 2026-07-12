defmodule Bregex do
  import Bitwise
  # Generate N decimal strings; count full matches of \A[0-9]+\z. Checksum = count.
  def main do
    n = String.to_integer(System.get_env("BENCH_N") || "20000")
    re = ~r/\A[0-9]+\z/

    {_, count} =
      Enum.reduce(1..n, {123_456_789, 0}, fn _, {x, c} ->
        x2 = band(x * 1_103_515_245 + 12_345, 0x7FFFFFFF)
        s = Integer.to_string(x2)
        s = if rem(x2, 2) == 0, do: s <> "x", else: s
        {x2, c + if(Regex.match?(re, s), do: 1, else: 0)}
      end)

    IO.puts(count)
  end
end
