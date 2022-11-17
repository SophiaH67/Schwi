import json
import amiami
from lib.amiami_item_to_embed import amiami_item_to_embed
from lib.events.AmiamiEvent import AmiamiEvent
from schwi.SchwiCog import SchwiCog
from discord.ext import commands
from discord import Embed


class Amiami(SchwiCog):
    dependencies = ["Settings", "EventManager"]

    @commands.group(name="amiami")
    async def amiami(self, ctx):
        pass

    @amiami.command(name="search", aliases=["s"])
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

    @amiami.command(name="monitor", aliases=["m"])
    async def amiami_monitor(self, ctx, query):
        search_terms = await self.search_terms
        if query in search_terms:
            await ctx.reply("Already monitoring that term.")
            return
        search_terms.append(query)
        await self.settings.set_setting("amiami_search_terms", json.dumps(search_terms))
        await ctx.reply(f"Added {query} to monitored terms.")

    @amiami.command(name="stop_monitoring", aliases=["stop", "sm"])
    async def amiami_stop_monitoring(self, ctx, query):
        search_terms = await self.search_terms
        if query not in search_terms:
            await ctx.reply("Not monitoring that term.")
            return
        search_terms.remove(query)
        await self.settings.set_setting("amiami_search_terms", json.dumps(search_terms))
        await ctx.reply("Stopped monitoring that term.")

    @property
    async def search_terms(self):
        return json.loads(
            await self.settings.get_or_create_setting("amiami_search_terms", "[]")
        )

    async def tick(self):
        search_terms = await self.search_terms
        for query in search_terms:
            results = amiami.search(query)
            for item in results.items:
                event = AmiamiEvent(self.schwi, item, query)
                self.eventmanager.emit(event)

    tick_delay = 3600
