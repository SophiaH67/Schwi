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
    return await ctx.run()
