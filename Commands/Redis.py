from redis.exceptions import ResponseError
from Classes.BaseCommand import BaseCommand


class Command(BaseCommand):
  aliases = ["redis"]

  async def run(self, ctx):
    res = self.schwi.redis.execute_command(" ".join(ctx.args))
    if res is None:
      return "None"
    return res.decode("utf-8")
