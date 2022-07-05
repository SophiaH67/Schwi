from dotenv import load_dotenv
from cogs.Db import Db
from cogs.UserManager import UserManager, UserNotAuthorizedException
import logging

logging.basicConfig(level=logging.INFO)
from cogs.settings import Settings

import os
from discord.ext import commands

load_dotenv()


class Schwi(commands.Bot):
    def __init__(self, *args, **kwargs):
        self.logger = logging.getLogger(self.__class__.__name__)
        super().__init__(os.getenv("PREFIX"), *args, **kwargs)

        # Load cogs
        self.add_cog(Db(self))
        self.add_cog(Settings(self))
        self.add_cog(UserManager(self))

        db = self.get_cog("Db")
        db.Base.metadata.create_all(db.engine)

    async def on_ready(self):
        self.logger.info("Logged on as {0}!".format(self.user))

    async def on_command_error(self, context, exception):
        if isinstance(exception, UserNotAuthorizedException):
            return await context.send("You are not authorized to use this command.")
        return await super().on_command_error(context, exception)


client = Schwi()
client.run(os.getenv("DISCORD_TOKEN"))
