from Classes.MessageContext import MessageContext


class Command:
  aliases = ["thanks"]

  def __init__(self, schwi):
    self.schwi = schwi

  async def run(self, ctx: MessageContext):
    print("ThanksCommand")
    await ctx.info(
      ["I don't know what I did, but no problem", "You're welcome?", "No problem"]
    )
