from hashlib import md5
from secrets import choice
from Classes.BaseCommand import BaseCommand
from Classes.Lib.ProofOfWork import ProofOfWork
from Classes.MessageContext import MessageContext
from Classes.PermissionsManager import PermissionLevel


class Command(BaseCommand):
  aliases = ["sudo"]

  async def run(self, ctx: MessageContext):
    ctx.permission_level = PermissionLevel.ADMIN
    if len(ctx.args) == 0:
      raise Exception("Usage: sudo <command>")
    ctx.command = ctx.args.pop(0)

    proof_of_work = ProofOfWork(ctx.message, 7)

    await ctx.info(
      f'Solve a proof of work with the string prefix of "{proof_of_work.string_prefix}" and the hash prefix of "{proof_of_work.hash_prefix}"'
    )

    await proof_of_work.wait_for_solve(ctx.schwi)

    return await ctx.run()
