from dotenv import load_dotenv

from cogs.settings import Settings

load_dotenv()
import os
from discord.ext import commands


class MyClient(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(os.getenv("PREFIX"), *args, **kwargs)

        # Load cogs
        self.add_cog(Settings(self))

    async def on_ready(self):
        print("Logged on as {0}!".format(self.user))


client = MyClient()
client.run(os.getenv("DISCORD_TOKEN"))
