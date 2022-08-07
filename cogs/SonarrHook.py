import logging
from discord.ext import commands
from discord import Message

from schwi.SchwiCog import SchwiCog


class SonarrHook(SchwiCog):
    """Whenever a message is posted in #log by Marine,
    tell jellyfin to scan all libraries
    """

    succes_colors = ["#3e6800", "#27c24c", "#000000"]

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if len(message.embeds) != 1:
            self.logger.debug(f"Embeds not 1: {len(message.embeds)}")
            return
        if not str(message.embeds[0].color) in self.succes_colors:
            self.logger.debug(f"Not a success message: {message.embeds[0].color}")
            return
        if not message.channel.name == "log":
            self.logger.debug(f"Not in #log: {message.channel.name}")
            return
        if not message.author.name == "Marine":
            self.logger.debug(f"Not Marine: {message.author.name}")
            return

        await self.schwi.get_cog("Jellyfin").refresh_all_libraries()
        # React with rocket emoji
        await message.add_reaction("🚀")
