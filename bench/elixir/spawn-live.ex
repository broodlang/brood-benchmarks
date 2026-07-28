defmodule Bspawnlive do
  # Hold N processes ALIVE at once, then release them all. The `spawn` row measures
  # fan-out throughput with units that exit immediately; this measures what it costs
  # to KEEP N parked — the process-per-connection shape. Peak RSS matters as much as
  # wall time. Checksum = N.
  def main do
    n = String.to_integer(System.get_env("BENCH_N") || "300000")
    parent = self()
    pids = for _ <- 1..n, do: spawn(fn -> receive do {:go, _} -> send(parent, {:r, 1}) end end)
    Enum.each(pids, fn p -> send(p, {:go, 1}) end)
    total = Enum.reduce(1..n, 0, fn _, acc -> receive do {:r, v} -> acc + v end end)
    IO.puts(total)
  end
end
