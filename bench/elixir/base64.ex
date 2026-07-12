defmodule Bbase64 do
  import Bitwise
  # Generate N bytes, base64 encode+decode. Checksum = (sum enc char codes + sum
  # decoded bytes) mod 2^31.
  def main do
    n = String.to_integer(System.get_env("BENCH_N") || "50000")

    {_, rbytes} =
      Enum.reduce(1..n, {123_456_789, []}, fn _, {x, acc} ->
        x2 = band(x * 1_103_515_245 + 12_345, 0x7FFFFFFF)
        {x2, [rem(x2, 256) | acc]}
      end)

    bin = :erlang.list_to_binary(Enum.reverse(rbytes))
    enc = Base.encode64(bin)
    dec = Base.decode64!(enc)
    enc_sum = Enum.reduce(:binary.bin_to_list(enc), 0, fn c, a -> rem(a + c, 2147483647) end)
    dec_sum = Enum.reduce(:binary.bin_to_list(dec), 0, fn c, a -> rem(a + c, 2147483647) end)
    IO.puts(rem(enc_sum + dec_sum, 2147483647))
  end
end
