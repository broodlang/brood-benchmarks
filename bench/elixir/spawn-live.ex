defmodule Bspawnlive do
  # Hold N units alive, then send each a message it must COPY. See the Brood port for
  # why the payload matters: without it the coroutine runtimes score by doing nothing.
  # On the BEAM the copy is what `send` already does. Checksum = N * (sum(payload) + 1).
  def main do
    n = String.to_integer(System.get_env("BENCH_N") || "300000")
    payload = Enum.to_list(0..15)
    parent = self()
    pids = for id <- 1..n, do: spawn(fn -> unit(parent, id) end)
    Enum.each(pids, fn p -> send(p, {:go, payload}) end)
    total = Enum.reduce(1..n, 0, fn _, acc -> receive do {:r, v} -> acc + v end end)
    IO.puts(total)
  end

  defp unit(parent, _id) do
    receive do
      {:go, p} -> send(parent, {:r, Enum.sum(p) + 1})
    end
  end
end
