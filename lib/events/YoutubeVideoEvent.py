from lib.format_seconds import format_seconds
from .SchwiEvent import SchwiEvent
from discord import Embed


class YoutubeVideoEvent(SchwiEvent):
    def __init__(self, schwi, video):
        self.video = video

        super().__init__(schwi)

    @property
    def uid(self):
        return self.video.video_id

    def as_embed(self):
        embed = Embed(
            title=self.video.title,
            description=f"{self.video.views} views - {format_seconds(self.video.length)}",
            url=self.video.watch_url,
            color=0xFF0000,
        )
        embed.add_field(
            name="Keywords", value=", ".join(self.video.keywords) or "No keywords"
        )
        embed.set_image(url=self.video.thumbnail_url)

        return embed

    def as_message(self):
        return (f"New video from {self.video.vid_info['videoDetails']['author']}!",)
