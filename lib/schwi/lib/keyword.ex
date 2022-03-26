defmodule Schwi.Lib.Keyword do
  def add_keyword(keyword, user_id) do
    {:ok, response} = Redix.command(:redix, ["sadd", "schwi:keyword:#{keyword}", user_id])
    response
  end

  def remove_keyword(keyword, user_id) do
    {:ok, response} = Redix.command(:redix, ["srem", "schwi:keyword:#{keyword}", user_id])
    response
  end

  def get_keywords(user_id) do
    user_id = "#{user_id}"
    {:ok, response} = Redix.command(:redix, ["keys", "schwi:keyword:*"])

    keyword_ids =
      Enum.map(response, fn keyword ->
        # Remove the prefix
        keyword = String.slice(keyword, 14, String.length(keyword))

        {String.to_atom(keyword), Schwi.Lib.Keyword.get_interested_users(keyword)}
      end)

    interested_keywords =
      Enum.filter(keyword_ids, fn keyword_id ->
        {_keyword, users} = keyword_id
        Enum.member?(users, user_id)
      end)

    Enum.map(interested_keywords, fn keyword_id ->
      {keyword, _users} = keyword_id
      keyword
    end)
  end

  def get_interested_users(keyword) do
    {:ok, ids} = Redix.command(:redix, ["smembers", "schwi:keyword:#{keyword}"])
    ids
  end

  def notify_keywords(msg) do
    content = String.downcase(msg.content)

    embed_content =
      if Enum.empty?(msg.embeds) do
        []
      else
        Enum.map(msg.embeds, fn embed ->
          # Add embed.title and embed.description to content
          String.downcase(embed.title) <> String.downcase(embed.description)
        end)
      end

    content = content <> Enum.join(embed_content, " ")

    # Replace ' and " with nothing
    content = String.replace(content, "'", "")
    content = String.replace(content, "\"", "")

    keywords = OptionParser.split(content)

    ids_list =
      Enum.map(keywords, fn keyword ->
        Schwi.Lib.Keyword.get_interested_users(keyword)
      end)

    ids_list = Enum.reject(ids_list, fn ids -> Enum.empty?(ids) end)
    ids_list = Enum.flat_map(ids_list, fn ids -> ids end)
    ids_list = MapSet.new(ids_list)
    ids_list = MapSet.delete(ids_list, "#{msg.author.id}")

    mentions_list =
      Enum.map(ids_list, fn id ->
        "<@!#{id}>"
      end)

    unless Enum.empty?(mentions_list) do
      Schwi.Lib.Message.info(
        msg,
        "#{Enum.join(mentions_list, " ")} you should be interested in this"
      )
    end
  end
end
