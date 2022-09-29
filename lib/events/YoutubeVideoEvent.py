from .SchwiEvent import SchwiEvent


class YoutubeVideoEvent(SchwiEvent):
    def __init__(self, schwi, video):
        self.video = video

        super().__init__(schwi)

    @property
    def uid(self):
        return self.video.video_id
