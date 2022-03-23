defmodule Schwi.CommandHandler do
  def handle(msg) do
    message = msg.content

    args = String.split(message, " ")
    {cmd, args} = List.pop_at(args, 0)

    try do
      module = String.to_existing_atom("Elixir.Schwi.Commands.#{cmd}")

      spawn(fn ->
        apply(module, :run, [msg, args])
      end)
    rescue
      _e in ArgumentError -> :noop
    end
  end
end
