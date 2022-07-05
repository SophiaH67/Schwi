from __future__ import annotations
from discord.ext import commands
from typing import TYPE_CHECKING
from sqlalchemy import Column, Integer, String

from sqlalchemy.orm.decl_api import DeclarativeMeta

from lib.find_ctx import find_ctx


if TYPE_CHECKING:
    from ..schwi import Schwi
    from cogs.Db import Db


class PermissionLevel:
    NONE = 0
    TRUSTED = 1
    ADMIN = 2


class UserNotAuthorizedException(Exception):
    pass


def minimum_permission_level(min_level):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            ctx = find_ctx(*args)

            user_manager: UserManager = ctx.bot.get_cog("UserManager")
            user = user_manager.get_or_create_user(ctx.author)
            if user is None:
                raise UserNotAuthorizedException()
            if user.permission_level < min_level:
                raise UserNotAuthorizedException()
            return await func(*args, **kwargs)

        return wrapper

    return decorator


class UserManager(commands.Cog):
    def __init__(self, schwi: Schwi):
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
        user = self.db.Session.query(self.db.User).filter(self.db.User.id == id).first()
        if user is None:
            user = self.db.User(id)
            self.db.Session.add(user)
        return user
