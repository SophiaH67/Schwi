import uuid
from lib.async_amiami import Item

from lib.amiami_item_to_embed import amiami_item_to_embed

from .SchwiEvent import SchwiEvent


class AmiamiEvent(SchwiEvent):
    item: Item

    def __init__(self, schwi, item: Item, monitored_term: str, **kwargs):
        self.item = item
        self.monitored_term = monitored_term

        super().__init__(schwi, **kwargs)

    @property
    def uid(self):
        # We already check duplication somewhere else, so we don't need to do it here
        return self.item.productCode + str(uuid.uuid4())

    def is_unique(self):
        return True

    def as_embed(self):
        embed = amiami_item_to_embed(self.item)
        embed.set_footer(text=f"Monitored term: {self.monitored_term}")
        return embed

    def as_message(self):
        return f'Item matching "{self.monitored_term}" is now in stock!'
