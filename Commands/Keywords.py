from Classes.BaseCommand import BaseCommand
from Classes.MessageContext import MessageContext


class Command(BaseCommand):
  aliases = ["keyword", "keywords", "kw"]

  async def run(self, ctx: MessageContext):
    subcommand = ctx.args[0] if len(ctx.args) > 0 else None
    if subcommand is None or not subcommand in ["add", "remove", "list"]:
      return await ctx.error(
        [
          "I don't understand what you want me to do.",
          "This is not enough information for me to be useful.",
        ]
      )
    if subcommand == "add":
      keyword = ctx.args[1]
      if keyword is None:
        return await ctx.error(
          [
            "I don't understand what you want me to do.",
            "This is not enough information for me to be useful.",
          ]
        )
      self.schwi.keyword_manager.add_keyword(keyword, str(ctx.message.author.id))
      await ctx.info(
        [
          f"Added keyword {keyword} to your list.",
          f"You are now interested in {keyword}. Hentai",
        ]
      )
    elif subcommand == "remove":
      keyword = ctx.args[1]
      if keyword is None:
        return await ctx.error(
          [
            "I don't understand what you want me to do.",
            "This is not enough information for me to be useful.",
          ]
        )
      self.schwi.keyword_manager.remove_keyword(keyword, str(ctx.message.author.id))
      await ctx.info(
        [
          f"Removed keyword {keyword} from your list.",
          f"Unlike the no-fly list, you are no longer on the {keyword} list.",
        ]
      )
    elif subcommand == "list":
      keywords = self.schwi.keyword_manager.get_keywords(str(ctx.message.author.id))
      keywords = ", ".join(keywords)
      if len(keywords) == 0:
        return await ctx.info(
          [
            "You have no keywords.",
            "You are not interested in any keywords.",
          ]
        )
      await ctx.info(
        [
          f"You are interested in the following keywords: {keywords}",
          f"You are interested in the following keywords: {keywords}",
        ],
      )
