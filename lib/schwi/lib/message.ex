defmodule Schwi.Lib.Message do
  alias Nostrum.Api

  def reply(msg, text) do
    Api.create_message(msg.channel_id,
      content: text,
      message_reference: %{message_id: msg.id}
    )
  end

  def success(msg, text) do
    response =
      Enum.random([
        "Answer: #{text}",
        "Response: #{text}"
      ])

    Schwi.Lib.Message.reply(msg, response)
  end

  def error(msg, text) do
    response =
      Enum.random([
        "Comprehension impossible: #{text}",
        "Incomprehensible: #{text}"
      ])

    Schwi.Lib.Message.reply(msg, response)
  end
end
