from lib.dataclasses.torrent import Torrent
from .SchwiEvent import SchwiEvent


class QbitEvent(SchwiEvent):
    event_name = "qbit"  # type: ignore

    def __init__(self, schwi, torrent: Torrent):
        self.torrent = torrent

        super().__init__(schwi)

    @property
    def uid(self):
        return self.torrent.hash
