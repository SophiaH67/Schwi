from Classes.MessageContext import MessageContext


class Command:
  aliases = ["hello"]

  def __init__(self, schwi):
    self.schwi = schwi

  async def run(self, ctx: MessageContext):
    await ctx.info(
      [
        "Hello",
        "Hi",
        "Konbanwa",
      ]
    )
