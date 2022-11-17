from lib.dataclasses.torrent import Torrent
from discord import Embed
from .SchwiEvent import SchwiEvent


class QbitEvent(SchwiEvent):
    def __init__(self, schwi, torrent: Torrent):
        self.torrent = torrent

        super().__init__(schwi)

    @property
    def uid(self):
        return self.torrent.hash

    def as_embed(self):
        return Embed(title=self.torrent.name, color=0x2F67BA)

    def as_message(self):
        return f"Torrent added!"
