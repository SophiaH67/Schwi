from Classes.BaseCommand import BaseCommand
from Classes.Exceptions.PermissionsException import PermissionsException
from Classes.MessageContext import MessageContext
from Classes.PermissionsManager import PermissionLevel


class Command(BaseCommand):
  aliases = ["demote"]

  async def run(self, ctx: MessageContext):
    if ctx.permission_level != PermissionLevel.ADMIN:
      raise PermissionsException()
    # Get first mentioned user
    if len(ctx.message.mentions) < 1:
      raise Exception("You must mention a user")
    user = ctx.message.mentions[0]
    self.schwi.permissions_manager.set_permissions(user.id, PermissionLevel.USER)
