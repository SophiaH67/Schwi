from __future__ import annotations
from discord.ext import commands
import discord
from typing import TYPE_CHECKING
from sqlalchemy import BigInteger, Column, Integer, String


from lib.minimum_permission_level import is_admin
from schwi.SchwiCog import SchwiCog


if TYPE_CHECKING:
    from ..main import Schwi
    from cogs.Db import Db


def user_factory(base):
    class User(base):
        __tablename__ = "users"
        id = Column(BigInteger, primary_key=True)
        permission_level = Column(Integer)
        name = Column(String)

        def __init__(self, id: int, name: str, permission_level: int = 0):
            self.id = id
            self.name = name
            self.permission_level = permission_level

    return User


class UserManager(SchwiCog):
    dependencies = ["Db"]
    models = [user_factory]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_or_create_user(self, member: discord.Member):
        user = self.db.Session.query(self.db.User).filter_by(id=member.id).first()
        if user is None:
            user = self.db.User(member.id, member.name)
            self.db.Session.add(user)
            self.db.Session.commit()
        return user

    @commands.command(name="set_permission_level")
    @is_admin
    async def set_permission_level(
        self, ctx, discord_user: discord.Member, permission_level
    ):
        self.logger.info(
            f"Setting {discord_user.name}'s permission level to {permission_level}"
        )
        user = self.get_or_create_user(discord_user)
        user.permission_level = permission_level
        self.db.Session.commit()
        await ctx.reply(
            f"Set {discord_user.display_name}'s permission level to {permission_level}"
        )
