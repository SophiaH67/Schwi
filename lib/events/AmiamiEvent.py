from amiami.amiami import Item
from discord import Embed

from lib.amiami_item_to_embed import amiami_item_to_embed

from .SchwiEvent import SchwiEvent


class AmiamiEvent(SchwiEvent):
    item: Item

    def __init__(self, schwi, item: Item, monitored_term: str):
        self.item = item
        self.monitored_term = monitored_term

        super().__init__(schwi)

    @property
    def uid(self):
        return self.item.productCode

    def as_embed(self):
        return amiami_item_to_embed(self.item)

    def as_message(self):
        return f'New item matching "{self.monitored_term}"!'
