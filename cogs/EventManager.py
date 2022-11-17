import json
from lib.events.AmiamiEvent import AmiamiEvent
from lib.events.QbitEvent import QbitEvent
from lib.events.SchwiEvent import SchwiEvent
from lib.events.SchwiEventListener import SchwiEventListener
from lib.events.YoutubeVideoEvent import YoutubeVideoEvent
from schwi.SchwiCog import SchwiCog
from discord.ext import commands
from promise import Promise
from lib.minimum_permission_level import is_trusted
import asyncio

events = [AmiamiEvent, QbitEvent, YoutubeVideoEvent]
event_dict = {}
for event in events:
    event_dict[event.__name__] = event


class EventManager(SchwiCog):
    listeners: dict[str, list[SchwiEventListener]] = {}
    dependencies = ["Settings"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on(self, event: type[SchwiEvent], callback):
        self.logger.debug(f"Adding event listener for event {event.__name__}")
        listener = SchwiEventListener(event.__name__, callback)
        if event in self.listeners:
            self.listeners[event.__name__].append(listener)
        else:
            self.listeners[event.__name__] = [listener]
        return listener

    def off(self, listener: SchwiEventListener):
        self.logger.debug(
            f"Removing event listener {listener.event_name}({listener.id})"
        )
        self.listeners[listener.event_name].remove(listener)

    def emit(self, event: SchwiEvent):
        if not event.__class__.__name__ in self.listeners:
            return
        for listener in self.listeners[event.__class__.__name__]:
            if not event.is_unique():
                continue
            ret = listener.callback(event)
            if asyncio.iscoroutine(ret):
                loop = asyncio.get_event_loop()
                loop.create_task(ret)

    def wait_for(self, event: type[SchwiEvent]):
        def resolver(resolve, reject):
            def callback(event):
                resolve(event)
                self.off(listener)

            listener = self.on(event, callback)

        return Promise(resolver)

    @property
    async def subscriptions(self):
        return json.loads(
            await self.settings.get_or_create_setting("subscriptions", json.dumps({}))
        )

    @commands.group(name="subsciptions", aliases=["subsciption", "subs", "sub"])
    async def subscriptions_command(self, ctx):
        pass

    @subscriptions_command.command(name="list", aliases=["l"])
    async def subscriptions_list(self, ctx):
        subs = await self.subscriptions
        msg = ""
        for event_name in iter(subs):
            msg += f"{event_name}: <#{subs[event_name]}>\n"
        await ctx.reply(msg)

    @subscriptions_command.command(name="add", aliases=["a"])
    @is_trusted
    async def subscriptions_add(self, ctx, event_name: str):
        subs = await self.subscriptions
        subs[event_name] = ctx.channel.id
        await self.settings.set_setting("subscriptions", json.dumps(subs))
        await self.refresh_subscriptions()
        await ctx.reply(f"Added {event_name} to subscriptions")

    @subscriptions_command.command(name="remove", aliases=["r"])
    @is_trusted
    async def subscriptions_remove(self, ctx, event_name: str):
        subs = await self.subscriptions
        del subs[event_name]
        await self.settings.set_setting("subscriptions", json.dumps(subs))
        await self.refresh_subscriptions()
        await ctx.reply(f"Removed {event_name} from subscriptions")

    local_subscriptions = {}

    async def refresh_subscriptions(self):
        subs = await self.subscriptions
        for event_name in iter(subs):
            if event_name in self.local_subscriptions:
                self.off(self.local_subscriptions[event_name])
            self.local_subscriptions[event_name] = self.on(
                event_dict[event_name], self.send_event
            )

    async def send_event(self, event: SchwiEvent):
        subs = await self.subscriptions
        channel_id = subs[event.__class__.__name__]
        channel = self.schwi.get_channel(channel_id)

        if channel is None:
            self.logger.error(
                f"Could not find channel {channel_id} for event {event.__class__.__name__}"
            )
            return

        embed = event.as_embed()
        message = event.as_message()

        if embed:
            await channel.send(message, embed=embed)
        else:
            await channel.send(message)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.refresh_subscriptions()
