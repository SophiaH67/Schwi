from discord.ext import commands
from discord import Embed
from lib.dataclasses.torrent import Torrent
from lib.events.QbitEvent import QbitEvent
from lib.format_seconds import format_seconds
from lib.minimum_permission_level import is_trusted
from qbittorrent import Client
import urllib.parse
import os

from schwi.SchwiCog import SchwiCog

# Copied from https://stackoverflow.com/questions/1094841/get-human-readable-version-of-file-size
# because for some reason python people don't make libraries for this
def sizeof_fmt(num, suffix="B"):
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"


class Qbit(SchwiCog):
    qb = Client(os.getenv("QBIT_URL"))
    qb.login()
    dependencies = ["EventManager", "Settings"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.eventmanager.on(QbitEvent, self.on_qbit_event)

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
            value = f"{torrent['state']}"
            name = torrent["name"]
            if torrent["dlspeed"] > 0 or torrent["upspeed"] > 0:
                speeds = []
                if torrent["dlspeed"] > 0:
                    speeds.append(f"DL: {sizeof_fmt(torrent['dlspeed'])}/s")
                if torrent["upspeed"] > 0:
                    speeds.append(f"UL: {sizeof_fmt(torrent['upspeed'])}/s")
                value += f" ({' | '.join(speeds)})"
            # If the torrent is still downloading, show an ETA
            if torrent["state"] == "downloading":
                name += f" ({format_seconds(torrent['eta'])})"
            embed.add_field(name=name, inline=True, value=value)
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

    tick_delay = 60

    async def tick(self):
        for torrent in self.qb.torrents():
            event = QbitEvent(self.schwi, Torrent.from_dict(torrent))
            self.eventmanager.emit(event)

    @property
    async def qbit_channel(self):
        return await self.settings.get_or_create_setting(
            "qbit_channel", "968977044673273917"
        )

    @property
    async def notifications_enable(self):
        return (
            await self.settings.get_or_create_setting("notifications_enable", "True")
        ).lower() == "true"

    async def on_qbit_event(self, event: QbitEvent):
        if not await self.notifications_enable:
            return
        self.logger.info(f"Got qbit event: {event.torrent.name}")
        channel = self.schwi.get_channel(int(await self.qbit_channel))
        if channel is None:
            raise Exception("Qbit channel not found")
        embed = Embed(title=event.torrent.name, color=0x2F67BA)
        await channel.send("Torrent added!", embed=embed)
