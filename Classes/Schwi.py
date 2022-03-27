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
    self.redis = redis.Redis(host="localhost", port=6379, db=0)
    self.keyword_manager = KeywordManager(self.redis)
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
    print(f"{message.author}: {message.content}")
    if message.author == self.user:
      return

    ctx = MessageContext(message, self)

    content = message.content.lower() + (
      # Add embeds if they exist
      " " + str(message.embeds[0].description)
      if len(message.embeds) > 0
      else ""
    )

    interested_users = self.keyword_manager.get_interested_users(content)
    if len(interested_users) > 0:
      ping_string = ", ".join(map(lambda x: f"<@{x}>", interested_users))
      await ctx.info(
        [
          f"{ping_string}, you should probably read this.",
          f"{ping_string}, you might be interested in this.",
          f"Oi onii-chan get over here {ping_string}.",
        ]
      )

    await ctx.run()
