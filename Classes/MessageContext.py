import random
from discord import Message
import shlex
import typing

if typing.TYPE_CHECKING:
  from Classes.Schwi import Schwi


class MessageContext:
  permission_level = None

  def __init__(self, message: Message, schwi: "Schwi"):
    self.schwi = schwi
    self.message = message

    self.args = shlex.split(str.replace(message.content, "'", "\\'"))
    if len(self.args) == 0:
      return
    self.command = self.args.pop(0)

    # Set methods
    self._reply = self.message.reply

  @property
  def lcommand(self):
    return self.command.lower()

  async def run(self):
    if self.permission_level is None:
      self.permission_level = await self.schwi.permissions_manager.get_permissions(
        self.message.author.id
      )
    if str.lower(self.lcommand) in self.schwi.commands:
      try:
        result = await self.schwi.commands[self.lcommand].run(self)
        if result is not None:
          await self.success(result)
      except Exception as e:
        await self.error(str(e))

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
