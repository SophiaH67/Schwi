from redis.exceptions import ResponseError
from Classes.BaseCommand import BaseCommand


class Command(BaseCommand):
  aliases = ["redis"]

  async def run(self, ctx):
    try:
      res = self.schwi.redis.execute_command(" ".join(ctx.args))
      if res is None:
        return await ctx.successs("None")
      await ctx.success(res.decode("utf-8"))
    except ResponseError as e:
      await ctx.error(str(e))
