from Classes.BaseCommand import BaseCommand
from Classes.MessageContext import MessageContext


class Command(BaseCommand):
  aliases = ["hello"]

  async def run(self, ctx: MessageContext):
    await ctx.info(
      [
        "Hello",
        "Hi",
        "Konbanwa",
      ]
    )
