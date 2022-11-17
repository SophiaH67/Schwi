import innertube
from discord.ext import commands
from discord import Embed
from lib.events.YoutubeVideoEvent import YoutubeVideoEvent
from lib.format_seconds import format_seconds
from schwi.SchwiCog import SchwiCog
from pytube import Channel


class Youtube(SchwiCog):
    client = innertube.InnerTube("WEB")

    dependencies = ["EventManager", "Settings"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @commands.group(name="youtube", aliases=["yt"])
    async def youtube_command(self, ctx):
        pass

    @youtube_command.command(name="search", aliases=["s"], help="Search youtube")
    async def youtube_search(self, ctx, query):
        search = self.client.search(query)
        videos = search["contents"]["twoColumnSearchResultsRenderer"][
            "primaryContents"
        ]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"]
        embeds = []
        i = 0
        while i < len(videos) and len(embeds) < 5:
            if not "videoRenderer" in videos[i]:
                i += 1
                continue
            video = videos[i]["videoRenderer"]
            embed = Embed(
                title=video["title"]["runs"][0]["text"],
                url="https://youtube.com/watch?v="
                + videos[i]["videoRenderer"]["videoId"],
                color=0xFF0000,
            )
            embed.set_image(
                url=videos[i]["videoRenderer"]["thumbnail"]["thumbnails"][-1]["url"]
            )
            embeds.append(embed)
            i += 1

        await ctx.reply(f"Found {search['estimatedResults']} results for {query}")
        for embed in embeds:
            await ctx.send(embed=embed)

    tick_delay = 3600 / 4

    async def tick(self):
        for channel_id in await self.yt_channels:
            channel = Channel(f"https://www.youtube.com/c/{channel_id}/videos")
            self.logger.error(f"Failed to get channel {channel_id}")
            for video in channel.videos:
                self.eventmanager.emit(YoutubeVideoEvent(self.schwi, video))
