from Classes.PermissionsManager import PermissionsManager
import config
import discord
import os
import importlib
import redis


from Classes.KeywordManager import KeywordManager
from Classes.MessageContext import MessageContext


class Schwi(discord.Client):
  commands = {}

  def __init__(self):
    super().__init__()
    self.redis = redis.Redis(host=config.redis_host, port=config.redis_port, db=0)
    self.keyword_manager = KeywordManager(self.redis)
    self.permissions_manager = PermissionsManager(self)
    self.load_commands()

  def load_commands(self):
    for file in os.listdir("./Commands"):
      if file.endswith(".py"):
        name = file[:-3]
        cmd_module = importlib.import_module(f"Commands.{name}")
        cmd_instance = cmd_module.Command(self)
        for alias in cmd_instance.aliases:
          self.commands[alias] = cmd_instance
        print(f"Loaded command {name}")

  async def on_ready(self):
    print(f"Schwi is ready as {self.user}")

  async def on_message(self, message):
    if message.author == self.user:
      return

    ctx = MessageContext(message, self)

    await self.keyword_manager.ping_interested_users(ctx)

    await ctx.run()
