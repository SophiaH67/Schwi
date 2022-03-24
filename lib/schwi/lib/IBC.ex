defmodule Schwi.Lib.IBC do
  # IBC is the Inter-Bot Communication library using Discord.
  def send_command(command, args) do
    text = command <> " " <> Enum.join(args, " ")

    {:ok, %Nostrum.Struct.Message{id: message_id}} =
      Schwi.Lib.Message.send(875_825_922_559_860_787, text)

    own_pid_string = Kernel.inspect(self())
    # Remove first 5 characters, which are #PID<
    own_pid = String.slice(own_pid_string, 5..-2)

    Redix.command(:redix, ["SET", "ibc:#{message_id}", own_pid])

    # Wait for a response from the other bots.
    receive do
      {:bot_reply, msg} -> msg
    end
  end

  def is_ibc_reply(msg) do
    if msg.message_reference != nil do
      %Nostrum.Struct.Message.Reference{message_id: reply_id} = msg.message_reference
      {:ok, response} = Redix.command(:redix, ["GET", "ibc:#{Integer.to_string(reply_id)}"])

      response != nil
    else
      false
    end
  end

  def handle_reply(msg) do
    %Nostrum.Struct.Message.Reference{message_id: reply_id} = msg.message_reference
    {:ok, response} = Redix.command(:redix, ["GET", "ibc:#{Integer.to_string(reply_id)}"])

    send(IEx.Helpers.pid(response), {:bot_reply, msg})
  end
end
