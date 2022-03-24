defmodule Schwi.Commands.Hello do
  def run(msg, _args) do
    Schwi.Lib.Message.info(
      msg,
      Enum.random([
        "Hello",
        "Hi",
        "Konbanwa",
        "Hey Hey!"
      ])
    )
  end
end
