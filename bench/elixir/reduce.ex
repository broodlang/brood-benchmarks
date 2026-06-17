defmodule Breduce do
  # higher-order fold: + applied per element (Enum.reduce with a passed fn, not Enum.sum).
  def main do
    n = String.to_integer(System.get_env("BENCH_N") || "5000000")
    IO.puts(Enum.reduce(0..(n - 1), 0, fn x, acc -> acc + x end))
  end
end
