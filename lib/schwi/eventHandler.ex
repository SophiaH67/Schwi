defmodule Schwi.EventHandler do
  use Nostrum.Consumer

  def start_link do
    Consumer.start_link(__MODULE__)
  end

  def handle_event({:MESSAGE_CREATE, msg, _ws_state}) do
    IO.puts("#{msg.author.username}: #{msg.content}")

    if Schwi.Lib.IBC.is_ibc_reply(msg) do
      Schwi.Lib.IBC.handle_reply(msg)
    else
      Schwi.CommandHandler.handle(msg)
    end
  end

  # Default event handler, if you don't include this, your consumer WILL crash if
  # you don't have a method definition for each event type.
  def handle_event(_event) do
    :noop
  end
end
