import logging
from discord.ext import commands
from discord import Message


class SonarrHook(commands.Cog):
    """Whenever a message is posted in #log by Marine,
    tell jellyfin to scan all libraries
    """

    def __init__(self, schwi):
        self.schwi = schwi
        self.logger = logging.getLogger(self.__class__.__name__)

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if not message.author.name == "Marine":
            return
        if len(message.embeds) != 1:
            return
        if not message.embeds[0].color == "#27c24c":
            return
        if not message.channel.name == "log":
            return


        await self.schwi.get_cog("Jellyfin").scan_all_libraries()
        # React with rocket emoji
        await message.add_reaction("🚀")
