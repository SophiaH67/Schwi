from discord.ext import commands
from discord import Embed
from lib.minimum_permission_level import is_trusted
import os
from homeassistant_api import Client

from schwi.SchwiCog import SchwiCog


class Homeassistant(SchwiCog):
    client = Client(os.getenv("HASS_URL"), os.getenv("HASS_TOKEN"))

    @commands.group(name="homeassisant", aliases=["ha", "hass"])
    @is_trusted
    async def homeassistant_command(self, ctx):
        pass

    @homeassistant_command.command(
        name="list", aliases=["l"], help="List homeassistant entities and their status"
    )
    async def homeassistant_list(self, ctx, group_id=None):
        groups = await self.client.async_get_entities()
        embed = Embed(title="Homeassistant Entities")

        for group in groups:
            if group_id is None or group_id == group.group_id:
                for entity in group.entities.values():
                    print(entity)
                    embed.add_field(
                        name=entity.entity_id,
                        value=entity.state.state,
                        inline=False,
                    )

        await ctx.reply(embed=embed)

    @homeassistant_command.command(
        name="groups", aliases=["g"], help="List homeassistant groups"
    )
    async def homeassistant_groups(self, ctx):
        groups = await self.client.async_get_entities()
        await ctx.reply(", ".join([group.group_id for group in groups]))

    @homeassistant_command.command(
        name="lights", aliases=["light"], help="Set a light to a given state"
    )
    async def homeassistant_lights(self, ctx, light_id, target_state):
        on_states = ["on", "true", "1"]
        off_states = ["off", "false", "0"]
        toggle_states = ["toggle", "t"]

        light = await self.client.async_get_entity(entity_id=light_id)

        if light is None:
            await ctx.reply(f"{light_id} not found")
            return

        self.logger.debug(f"{light_id}: {light.state.state}")
        light_domain = self.client.get_domain("light")

        if target_state in on_states:
            await light_domain.turn_on(entity_id=light_id)
            await ctx.reply(f"{light_id} turned on")
        elif target_state in off_states:
            await light_domain.turn_off(entity_id=light_id)
            await ctx.reply(f"{light_id} turned off")
        elif target_state in toggle_states:
            await light_domain.toggle(entity_id=light_id)
            await ctx.reply(f"{light_id} toggled")
        else:
            await ctx.reply(f"Unknown state {target_state}")
