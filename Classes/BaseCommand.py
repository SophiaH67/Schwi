import typing
from Classes.MessageContext import MessageContext
from abc import abstractmethod

if typing.TYPE_CHECKING:
  from Classes.Schwi import Schwi


class BaseCommand:
  aliases = ["hello"]

  def __init__(self, schwi: "Schwi"):
    self.schwi = schwi

  @abstractmethod
  async def run(self, ctx: MessageContext):
    pass
