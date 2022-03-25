defmodule Schwi.Commands.Why do
  def run(msg, _args) do
    {result, response} = Schwi.Lib.GPT3.get_completion(msg.content)

    case result do
      :ok ->
        Schwi.Lib.Message.success(msg, response)

      :error ->
        Schwi.Lib.Message.error(msg, response)
    end
  end
end
