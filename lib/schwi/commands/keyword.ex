defmodule Schwi.Commands.Keyword do
  def run(msg, args) do
    # String.downcase all args
    args = Enum.map(args, fn arg -> String.downcase(arg) end)
    {subcommand, args} = List.pop_at(args, 0)
    subcommand = String.to_existing_atom(subcommand)
    Schwi.Commands.Keyword.handle_subcommand({msg, subcommand, args})
  end

  def handle_subcommand({msg, :add, args}) do
    args =
      Enum.map(args, fn arg ->
        response = Schwi.Lib.Keyword.add_keyword(arg, msg.author.id)

        if response == 0 do
          nil
        else
          arg
        end
      end)

    # Remove all nil values
    args = Enum.filter(args, fn arg -> arg end)

    if Enum.empty?(args) do
      Schwi.Lib.Message.error(msg, "No keywords added")
    else
      Schwi.Lib.Message.success(msg, "#{Enum.join(args, ",")} added to your keywords")
    end
  end

  def handle_subcommand({msg, :remove, args}) do
    for arg <- args do
      Schwi.Lib.Keyword.remove_keyword(arg, msg.author.id)
    end

    Schwi.Lib.Message.success(
      msg,
      "Removed keywords: #{Enum.join(args, ", ")} from your keywords."
    )
  end

  def handle_subcommand({msg, :list, _args}) do
    keywords = Schwi.Lib.Keyword.get_keywords(msg.author.id)

    if Enum.empty?(keywords) do
      Schwi.Lib.Message.error(msg, "You have no keywords")
    else
      Schwi.Lib.Message.success(msg, "#{Enum.join(keywords, ",")} are your highlighted keywords")
    end
  end
end
