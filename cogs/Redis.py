import os
from redis import Redis as RedisClient
from schwi.SchwiCog import SchwiCog
from lib.minimum_permission_level import is_admin
from discord.ext import commands


class RedisMeta(type(SchwiCog), type(RedisClient)):
    pass


class Redis(SchwiCog, RedisClient, metaclass=RedisMeta):
    def __init__(self, *args, **kwargs):
        SchwiCog.__init__(self, *args, **kwargs)
        RedisClient.__init__(
            self, host=os.getenv("REDIS_HOST") or "localhost", port=6379, db=0
        )

    @commands.group(name="redis", aliases=["r"])
    @is_admin
    async def redis(self, ctx):
        pass

    @redis.command(name="get", aliases=["g"], help="get a redis key")
    async def get_key(self, ctx, key):
        await ctx.reply(self.get(key) or "None")

    @redis.command(name="set", aliases=["s"], help="set a redis key")
    async def set_key(self, ctx, key, value):
        await ctx.reply(self.set(key, value))

    @redis.command(name="delete", aliases=["d"], help="delete a redis key")
    async def delete_key(self, ctx, key):
        await ctx.reply(self.delete(key))

    @redis.command(name="list", aliases=["ls"], help="list all redis keys")
    async def list_keys(self, ctx):
        str_keys = []
        for key in self.keys():
            key = key.decode("utf-8")
            if key.startswith("event:"):
                continue
            str_keys.append(key)
        if len(str_keys) == 0:
            await ctx.reply("Uh oh, the database appears to be empty!")
        else:
            await ctx.reply(
                "The following keys are available:```\n" + "\n".join(str_keys) + "```"
            )
