import json
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
        self.eventmanager.on(YoutubeVideoEvent, self.on_youtube_video_event)

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

    @property
    async def yt_channel(self):
        return await self.settings.get_or_create_setting(
            "yt_channel", "879030591692079154"
        )

    @property
    async def yt_channels(self):
        channels = await self.settings.get_or_create_setting(
            "yt_channels", "ZackFreedman,UnmeiIdols"
        )
        return channels.split(",")

    @property
    async def notifications_enable(self):
        return (
            await self.settings.get_or_create_setting("notifications_enable", "True")
        ).lower() == "true"

    tick_delay = 60

    async def tick(self):
        for channel_id in await self.yt_channels:
            channel = Channel(f"https://www.youtube.com/c/{channel_id}/videos")
            for video in channel.videos:
                self.eventmanager.emit(YoutubeVideoEvent(self.schwi, video))

    async def on_youtube_video_event(self, event: YoutubeVideoEvent):
        if not await self.notifications_enable:
            print("Notifications disabled, skipping")
            return
        discord_channel = self.schwi.get_channel(int(await self.yt_channel))
        if not discord_channel:
            raise Exception("Channel not found")

        embed = Embed(
            title=event.video.title,
            description=f"{event.video.views} views - {format_seconds(event.video.length)}",
            url=event.video.watch_url,
            color=0xFF0000,
        )
        embed.add_field(
            name="Keywords", value=", ".join(event.video.keywords) or "No keywords"
        )
        embed.set_image(url=event.video.thumbnail_url)
        await discord_channel.send(
            f"New video from {event.video.vid_info['videoDetails']['author']}!",
            embed=embed,
        )
