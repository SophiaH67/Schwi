defmodule Schwi.Application do
  # See https://hexdocs.pm/elixir/Application.html
  # for more information on OTP Applications
  @moduledoc false

  use Application

  @impl true
  def start(_type, _args) do
    children = [
      # Starts a worker by calling: Schwi.Worker.start_link(arg)
      {Redix, name: :redix},
      {Schwi.Worker, name: :worker},
      {Schwi.CommandHandler, name: :command_handler}
    ]

    # See https://hexdocs.pm/elixir/Supervisor.html
    # for other strategies and supported options
    opts = [strategy: :one_for_one, name: Schwi.Supervisor]
    Supervisor.start_link(children, opts)
  end
end
