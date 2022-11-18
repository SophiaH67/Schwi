import json
import amiami
from amiami.amiami import Item
from lib.amiami_item_to_embed import amiami_item_to_embed
from lib.events.AmiamiEvent import AmiamiEvent
from schwi.SchwiCog import SchwiCog
from discord.ext import commands
from sqlalchemy import Boolean, Column, String


def amiamiItem_factory(base):
    class AmiamiItem(base):
        __tablename__ = "amiami_items"
        productURL = Column(String)
        productName = Column(String)
        price = Column(String)
        productCode = Column(String, primary_key=True)
        availability = Column(String)
        instock = Column(Boolean)

    return AmiamiItem


class Amiami(SchwiCog):
    dependencies = ["Settings", "EventManager"]
    models = [amiamiItem_factory]

    @commands.group(name="amiami")
    async def amiami_cmd(self, ctx):
        pass

    @amiami_cmd.command(name="search", aliases=["s"])
    async def amiami_search(self, ctx, query, limit="1"):
        limit = int(limit)
        results = amiami.search("fumofumo plush")
        i = 0
        for item in results.items:
            i += 1
            embed = amiami_item_to_embed(item)
            await ctx.reply(embed=embed)
            if i >= limit:
                break

    @amiami_cmd.command(name="monitor", aliases=["m"])
    async def amiami_monitor(self, ctx, query):
        search_terms = await self.search_terms
        if query in search_terms:
            await ctx.reply("Already monitoring that term.")
            return
        search_terms.append(query)
        await self.settings.set_setting("amiami_search_terms", json.dumps(search_terms))
        await self.tick_query(query, dry=True)
        await ctx.reply(f"Added {query} to monitored terms.")

    @amiami_cmd.command(name="stop_monitoring", aliases=["stop", "sm"])
    async def amiami_stop_monitoring(self, ctx, query):
        search_terms = await self.search_terms
        if query not in search_terms:
            await ctx.reply("Not monitoring that term.")
            return
        search_terms.remove(query)
        await self.settings.set_setting("amiami_search_terms", json.dumps(search_terms))
        await ctx.reply("Stopped monitoring that term.")

    @amiami_cmd.command(name="list", aliases=["l"])
    async def amiami_list(self, ctx):
        search_terms = await self.search_terms
        nl = "\n"
        await ctx.reply(f"Currently monitoring: ```{nl}{nl.join(search_terms)}```")

    @property
    async def search_terms(self):
        return json.loads(
            await self.settings.get_or_create_setting("amiami_search_terms", "[]")
        )

    async def tick(self):
        search_terms = await self.search_terms
        for query in search_terms:
            await self.tick_query(query)

    async def save_amiami_item_to_db(self, item: Item):
        old_item = self.db.Session.query(self.db.AmiamiItem).get(item.productCode)

        if old_item is None:
            self.logger.info(f"Found new item: {item.productCode}")
            self.db.Session.add(
                self.db.AmiamiItem(
                    productURL=item.productURL,
                    productName=item.productName,
                    price=item.price,
                    productCode=item.productCode,
                    availability=item.availability,
                    instock=item.flags["instock"],
                )
            )
        else:
            old_item.productURL = item.productURL
            old_item.productName = item.productName
            old_item.price = item.price
            old_item.availability = item.availability
            old_item.instock = item.flags["instock"]
        self.db.Session.commit()

    async def tick_query(self, query: str, dry=False):
        results = amiami.search(query)
        for item in results.items:
            old_item = self.db.Session.query(self.db.AmiamiItem).get(item.productCode)

            # If item is now in stock, and wasn't before(or if it's a new item)
            if item.flags["instock"] and (old_item is None or not old_item.instock):
                self.logger.info(f"Found new in stock item: {item.productCode}")

                await self.save_amiami_item_to_db(item)

                event = AmiamiEvent(self.schwi, item, query, dry=dry)
                self.eventmanager.emit(event)

    tick_delay = 3600
