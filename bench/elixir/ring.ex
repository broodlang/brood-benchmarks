defmodule Bring do
  # A ring of N processes; a token travels around +1/hop for LAPS laps
  # (N*LAPS hops). Checksum = N*LAPS.
  def node_setup(total, parent) do
    receive do
      {:next, nxt} -> node_loop(nxt, total, parent)
    end
  end

  def node_loop(nxt, total, parent) do
    receive do
      v when v >= total -> send(parent, {:done, v})
      v -> send(nxt, v + 1); node_loop(nxt, total, parent)
    end
  end

  def main do
    n = String.to_integer(System.get_env("BENCH_N") || "200")
    laps = 5000
    total = n * laps
    parent = self()
    pids = for _ <- 1..n, do: spawn(fn -> node_setup(total, parent) end)
    wire(pids, hd(pids))
    send(hd(pids), 0)
    receive do {:done, v} -> IO.puts(v) end
  end

  defp wire([last], head), do: send(last, {:next, head})
  defp wire([a, b | rest], head) do
    send(a, {:next, b})
    wire([b | rest], head)
  end
end
