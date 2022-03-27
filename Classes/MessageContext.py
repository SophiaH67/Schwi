import random
from discord import Message
import shlex
import typing

if typing.TYPE_CHECKING:
  from Classes.Schwi import Schwi


class MessageContext:
  def __init__(self, message: Message, schwi: "Schwi"):
    self.schwi = schwi
    self.message = message

    self.args = shlex.split(str.replace(message.content, "'", "\\'"))
    self.command = self.args.pop()

    # Set methods
    self._reply = self.message.reply

  async def run(self):
    if str.lower(self.command) in self.schwi.commands:
      await self.schwi.commands[self.command].run(self)

  def _get_text(self, message: str | list[str]):
    if isinstance(message, str):
      return message
    else:
      return random.choice(message)

  def info(self, message):
    message = self._get_text(message)
    text = self._get_text(["Info: ", "Information: ", "Notice: "]) + message
    return self._reply(text)

  def error(self, message):
    message = self._get_text(message)
    text = (
      self._get_text(["Error: ", "Comprehension impossible: ", "Incomprehensible: "])
      + message
    )
    return self._reply(text)

  def success(self, message):
    message = self._get_text(message)
    text = self._get_text(["Success: ", "Answer: ", "Response: "]) + message
    return self._reply(text)
