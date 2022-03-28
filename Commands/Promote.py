from Classes.BaseCommand import BaseCommand
from Classes.Exceptions.PermissionsException import PermissionsException
from Classes.MessageContext import MessageContext
from Classes.PermissionsManager import PermissionLevel


class Command(BaseCommand):
  aliases = ["promote"]

  async def run(self, ctx: MessageContext):
    if ctx.permission_level != PermissionLevel.ADMIN:
      raise PermissionsException()
    if len(ctx.message.mentions) < 1:
      raise Exception("You must mention a user")
    user = ctx.message.mentions[0]
    self.schwi.permissions_manager.set_permissions(user.id, PermissionLevel.ADMIN)
    return f"{user.mention} is now an admin"
