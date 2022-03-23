defmodule Schwi.Worker do
  use GenServer

  def start_link(state) do
    GenServer.start_link(__MODULE__, state, name: __MODULE__)
  end

  def init(init_arg) do
    {:ok, msg} = Redix.command(:redix, ["PING"])
    IO.puts msg
    {:ok, init_arg}
  end

end
