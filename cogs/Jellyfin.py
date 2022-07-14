import logging
from discord.ext import commands
import os
import requests
from lib.minimum_permission_level import is_trusted


class Jellyfin(commands.Cog):
    def __init__(self, schwi):
        self.schwi = schwi
        self.logger = logging.getLogger(self.__class__.__name__)
        self.jellyfin_url = "https://jellyfin.marnixah.com"
        self.jellyfin_api_key = os.environ.get("JELLYFIN_API_KEY")

    def refresh_all_libraries(self):
        self.logger.info("Refreshing all libraries")
        url = self.jellyfin_url + "/Library/Refresh"
        headers = {
            "X-MediaBrowser-Token": self.jellyfin_api_key,
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        res = requests.post(url, headers=headers)
        self.logger.debug(f"Response: ({res.status_code}) {res.text}")
        return res.ok

    @commands.group(name="jellyfin", aliases=["jf"])
    @is_trusted
    async def jellyfin_command(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.reply("No subcommand given.")

    @jellyfin_command.command(name="refresh", aliases=["r"])
    async def jellyfin_refresh(self, ctx):
        if self.refresh_all_libraries():
            await ctx.reply("Refreshed all libraries")
        else:
            await ctx.reply("Failed to refresh libraries")
