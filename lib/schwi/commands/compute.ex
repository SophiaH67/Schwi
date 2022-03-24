defmodule Schwi.Commands.Compute do
  alias Nostrum.Api

  def run(msg, args) do
    query = Enum.join(args, " ")
    {result, response} = Schwi.Lib.GPT3.get_completion(query)

    text =
      case result do
        :ok ->
          Enum.random([
            "Answer: #{response}",
            "Response: #{response}"
          ])

        :error ->
          Enum.random([
            "Comprehension impossible: #{response}",
            "Incomprehensible: #{response}"
          ])
      end

    Api.create_message(msg.channel_id,
      content: text,
      message_reference: %{message_id: msg.id}
    )
  end
end
