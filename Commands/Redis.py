from Classes.BaseCommand import BaseCommand


class Command(BaseCommand):
  aliases = ["redis"]

  async def run(self, ctx):
    res = self.schwi.redis.execute_command(" ".join(ctx.args))
    if res is None:
      return "None"
    if isinstance(res, bytes):
      return res.decode("utf-8")
    if isinstance(res, list):
      return ", ".join(res)
    return res
