from __future__ import annotations
import logging
from discord.ext import commands
import discord
from typing import TYPE_CHECKING
from sqlalchemy import Column, Integer, String

from sqlalchemy.orm.decl_api import DeclarativeMeta

from lib.minimum_permission_level import is_admin


if TYPE_CHECKING:
    from ..schwi import Schwi
    from cogs.Db import Db


class UserManager(commands.Cog):
    def __init__(self, schwi: Schwi):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.schwi = schwi
        self.db: Db = schwi.get_cog("Db")
        base: DeclarativeMeta = self.db.Base
        # Register the User class with the Db class.
        class User(base):
            __tablename__ = "users"
            id = Column(String, primary_key=True)
            permission_level = Column(Integer)

            def __init__(self, id: str, permission_level: int = 0):
                self.id = id
                self.permission_level = permission_level

        self.db.User = User

    def get_or_create_user(self, id: str):
        user = self.db.Session.query(self.db.User).filter_by(id=id).first()
        if user is None:
            user = self.db.User(id)
            self.db.Session.add(user)
        return user

    @commands.command(name="set_permission_level")
    @is_admin
    async def set_permission_level(
        self, ctx, discord_user: discord.Member, permission_level
    ):
        self.logger.info(
            f"Setting {discord_user.name}'s permission level to {permission_level}"
        )
        user = self.get_or_create_user(discord_user.id)
        user.permission_level = permission_level
        self.db.Session.commit()
        await ctx.send(
            f"Set {discord_user.display_name}'s permission level to {permission_level}"
        )
