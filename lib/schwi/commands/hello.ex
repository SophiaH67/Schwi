defmodule Schwi.Commands.Hello do
  alias Nostrum.Api

  def run(msg, _args) do
    if Logger.level() == :info do
      Api.create_message(msg.channel_id, "Hello, #{msg.author.username}!")
    end
  end
end
