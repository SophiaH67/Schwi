defmodule Schwi.CommandHandler do
  def handle(msg) do
    message = msg.content

    args = Schwi.CommandHandler.parse_args(message)
    {cmd, args} = List.pop_at(args, 0)

    try do
      cmd = cmd || ""
      cased_cmd = Recase.to_pascal(String.downcase(cmd))
      module = String.to_existing_atom("Elixir.Schwi.Commands.#{cased_cmd}")

      spawn(fn ->
        apply(module, :run, [msg, args])
      end)
    rescue
      _e in ArgumentError -> :noop
    end
  end

  def parse_args(message) do
    OptionParser.split(message)
  end
end
