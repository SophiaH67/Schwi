from Classes.BaseCommand import BaseCommand
from Classes.MessageContext import MessageContext


class Command(BaseCommand):
  aliases = ["thanks"]

  async def run(self, ctx: MessageContext):
    print("ThanksCommand")
    await ctx.info(
      ["I don't know what I did, but no problem", "You're welcome?", "No problem"]
    )
