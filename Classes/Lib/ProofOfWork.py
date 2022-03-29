from hashlib import md5
from random import choice

from discord import Message


class ProofOfWork:
  def __init__(self, message: Message, difficulty: int):
    self.message = message
    self.difficulty = difficulty

    self.hash_prefix = "".join(
      choice("0123456789abcdef") for _ in range(self.difficulty)
    )
    self.string_prefix = choice(["Gaming", "SchwiIsAwesome",]) + "".join(
      map(lambda x: choice(list("abcdefghijklmnopqrstuvwxyz")), range(self.difficulty))
    )

  def dcheck(self, message: Message):
    return (
      message.author == self.message.author and message.channel == self.message.channel
    )

  def check(self, message: Message):
    return (
      md5(message.content.encode("utf-8")).hexdigest()[: self.difficulty]
      == self.hash_prefix
    )

  async def wait_for_solve(self, schwi):
    msg = await schwi.wait_for("message", check=self.dcheck)
    if not self.check(msg):
      raise Exception("Proof of work failed")
    return True
