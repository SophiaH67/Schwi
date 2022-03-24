defmodule Schwi.Commands.Redis do
  def run(msg, args) do
    joined_args = Enum.join(args, " ")

    if String.trim(joined_args) == "" do
      Schwi.Lib.Message.error(msg, "Provide a redis command to run.")
    else
      trimmed_args = Enum.map(args, fn arg -> String.trim(arg) end)
      response = Redix.command(:redix, trimmed_args)

      case response do
        {:ok, response} ->
          Schwi.Lib.Message.success(msg, response)

        {:error, %Redix.Error{message: message}} ->
          Schwi.Lib.Message.error(msg, message)
      end
    end
  end
end
