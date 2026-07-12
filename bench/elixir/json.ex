defmodule Bjson do
  import Bitwise
  # Build N records, JSON.encode! then JSON.decode! (Elixir's built-in JSON),
  # checksum sum of "v" mod 2^31.
  def main do
    n = String.to_integer(System.get_env("BENCH_N") || "2000")

    {_, arr} =
      Enum.reduce(1..n, {123_456_789, []}, fn i, {x, acc} ->
        x2 = band(x * 1_103_515_245 + 12_345, 0x7FFFFFFF)
        {x2, [%{"id" => i - 1, "v" => x2, "name" => "item", "ok" => rem(x2, 2) == 0} | acc]}
      end)

    parsed = JSON.decode!(JSON.encode!(arr))
    total = Enum.reduce(parsed, 0, fn o, acc -> rem(acc + o["v"], 2147483647) end)
    IO.puts(total)
  end
end
