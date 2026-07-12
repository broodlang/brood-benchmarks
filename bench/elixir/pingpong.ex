defmodule Bpingpong do
  # Two processes bounce a token N round trips. Checksum = N.
  def responder(parent) do
    receive do
      {:ping, ^parent} ->
        send(parent, :pong)
        responder(parent)

      :stop ->
        :ok
    end
  end

  def main do
    n = String.to_integer(System.get_env("BENCH_N") || "100000")
    parent = self()
    pong = spawn(fn -> responder(parent) end)
    k = ping(pong, n, 0)
    send(pong, :stop)
    IO.puts(k)
  end

  defp ping(_pong, n, n), do: n

  defp ping(pong, n, k) do
    send(pong, {:ping, self()})
    receive do
      :pong -> ping(pong, n, k + 1)
    end
  end
end
