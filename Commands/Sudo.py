from hashlib import md5
from secrets import choice
from Classes.BaseCommand import BaseCommand
from Classes.MessageContext import MessageContext
from Classes.PermissionsManager import PermissionLevel


class Command(BaseCommand):
  aliases = ["sudo"]

  async def run(self, ctx: MessageContext):
    ctx.permission_level = PermissionLevel.ADMIN
    if len(ctx.args) == 0:
      raise Exception("Usage: sudo <command>")
    ctx.command = ctx.args.pop(0)

    # Proof of work
    difficulity = 6
    # hash_prefix is a random hex string of length difficulity
    hash_prefix = "".join(choice("0123456789abcdef") for _ in range(difficulity))
    string_prefix = choice(["Gaming", "SchwiIsAwesome",]) + "".join(
      map(lambda x: choice(list("abcdefghijklmnopqrstuvwxyz")), range(difficulity))
    )

    await ctx.info(
      f'Solve a proof of work with the string prefix of "{string_prefix}" and the hash prefix of "{hash_prefix}"'
    )

    def check(m):
      return m.author == ctx.message.author and m.channel == ctx.message.channel

    msg = await self.schwi.wait_for("message", check=check)
    if md5(msg.content.encode("utf-8")).hexdigest()[:difficulity] != hash_prefix:
      raise Exception("Incorrect proof of work")

    return await ctx.run()
