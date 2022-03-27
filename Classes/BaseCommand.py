from Classes.MessageContext import MessageContext
from abc import abstractmethod


class BaseCommand:
  aliases = ["hello"]

  def __init__(self, schwi):
    self.schwi = schwi

  @abstractmethod
  async def run(self, ctx: MessageContext):
    pass
