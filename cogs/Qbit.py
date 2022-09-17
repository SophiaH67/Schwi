import logging
from discord.ext import commands
from discord import Embed
from lib.minimum_permission_level import is_trusted
from qbittorrent import Client
import urllib.parse
import os

from schwi.SchwiCog import SchwiCog


class Qbit(SchwiCog):
    qb = Client(os.getenv("QBIT_URL"))
    qb.login()

    @commands.group(name="qbit", aliases=["qb"])
    async def qbit_command(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.reply("No subcommand given.")

    @qbit_command.command(
        name="list", aliases=["l"], help="List the latest 20 torrents and their status"
    )
    async def qbit_list(self, ctx, limit=18):
        if limit > 18:
            limit = 18
        torrents = self.qb.torrents()
        # Sort torrents by ["added_on"]
        torrents.sort(key=lambda x: -x["added_on"])
        embed = Embed(title="Qbit Torrents")
        for torrent in torrents[:limit]:
            embed.add_field(
                name=torrent["name"],
                inline=True,
                value=f"{torrent['state']} - {round(torrent['progress'] * 100, 1)}%",
            )
        await ctx.reply(embed=embed)

    @qbit_command.command(name="add", aliases=["a"], help="Add a torrent to qbit")
    @is_trusted
    async def qbit_add(self, ctx, magnet_link, category="misc"):
        magnet_link = urllib.parse.unquote_plus(magnet_link)
        self.logger.info(f"Adding {magnet_link} to qbit")
        res = self.qb.download_from_link(magnet_link, category=category)
        self.logger.debug(f"Got response from qbittorrent: {res}")
        if str(res) == "Fails.":
            await ctx.reply("Failed to add torrent.")
        else:
            await ctx.reply("Torrent added.")
