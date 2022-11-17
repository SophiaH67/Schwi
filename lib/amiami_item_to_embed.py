from discord import Embed
from amiami.amiami import Item


def amiami_item_to_embed(item: Item):
    embed = Embed(
        title=item.productName,
        url=item.productURL,
    )
    embed.set_image(url=item.imageURL)
    embed.add_field(name="Price", value=f"{item.price} JPY")
    embed.add_field(name="Availability", value=item.availability)
    return embed
