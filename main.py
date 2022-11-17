from dotenv import load_dotenv
from cogs.Amiami import Amiami
from cogs.EventManager import EventManager
from cogs.Redis import Redis
from cogs.Youtube import Youtube

load_dotenv()

from cogs.Jellyfin import Jellyfin
from cogs.Qbit import Qbit
from cogs.SonarrHook import SonarrHook
from cogs.Mood import Mood
from cogs.Homeassistant import Homeassistant

from cogs.Db import Db
from cogs.UserManager import UserManager
from cogs.Context import Context
from cogs.NaturalLanguage import NaturalLanguage
import logging

logging.basicConfig(level=logging.DEBUG)
logging.getLogger("pytube").setLevel(logging.INFO)
logging.getLogger("urllib3").setLevel(logging.INFO)
logging.getLogger("discord").setLevel(logging.INFO)
from cogs.Settings import Settings

import os
from discord.ext import commands


class Schwi(commands.Bot):
    def __init__(self, *args, **kwargs):
        self.logger = logging.getLogger(self.__class__.__name__)
        super().__init__(os.getenv("PREFIX"), *args, **kwargs)

        # Load cogs
        self.add_cog(Db(self))
        self.add_cog(Settings(self))
        self.add_cog(Redis(self))
        self.add_cog(EventManager(self))
        self.add_cog(SonarrHook(self))
        self.add_cog(UserManager(self))
        # self.add_cog(Youtube(self))
        self.add_cog(Context(self))
        # self.add_cog(NaturalLanguage(self))
        # self.add_cog(Docker(self))
        self.add_cog(Qbit(self))
        self.add_cog(Jellyfin(self))
        self.add_cog(Mood(self))
        self.add_cog(Homeassistant(self))
        self.add_cog(Amiami(self))

        db = self.get_cog("Db")
        db.Base.metadata.create_all(db.engine)

    async def on_ready(self):
        self.logger.info("Logged on as {0}!".format(self.user))

    async def on_command_error(self, ctx, exception):
        raise exception
        await super().on_command_error(ctx, exception)


client = Schwi()
client.run(os.getenv("DISCORD_TOKEN"))
