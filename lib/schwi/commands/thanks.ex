defmodule Schwi.Commands.Thanks do
  def run(msg, args) do
    # If "Schwi" is in any of the arguments, then we'll say thanks.
    if Enum.any?(args, fn arg -> String.downcase(arg) == "schwi" end) do
      Schwi.Lib.Message.info(
        msg,
        Enum.random([
          "I don't know what I did, but no problem",
          "You're welcome?",
          "No problem"
        ])
      )
    end
  end
end
