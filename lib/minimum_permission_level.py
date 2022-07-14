from __future__ import annotations
from discord.ext import commands
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from cogs.UserManager import UserManager


class PermissionLevel:
    NONE = 0
    TRUSTED = 1
    ADMIN = 2


def predicate_factory(permission_level: int):
    def predicate(ctx):
        user_manager: UserManager = ctx.bot.get_cog("UserManager")
        user = user_manager.get_or_create_user(ctx.author)
        if user.permission_level < permission_level:
            return False
        return True

    return predicate


is_admin = commands.check(predicate_factory(PermissionLevel.ADMIN))
is_trusted = commands.check(predicate_factory(PermissionLevel.TRUSTED))
