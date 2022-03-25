defmodule Schwi.Commands.What do
  def run(msg, args) do
    query = "What " <> Enum.join(args, " ")
    {result, response} = Schwi.Lib.GPT3.get_completion(query)

    case result do
      :ok ->
        Schwi.Lib.Message.success(msg, response)

      :error ->
        Schwi.Lib.Message.error(msg, response)
    end
  end
end