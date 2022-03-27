import discord
import os
import importlib
import redis

from Classes.MessageContext import MessageContext


class Schwi(discord.Client):
  commands = {}

  def __init__(self):
    super().__init__()
    self.redis = redis.Redis(host="localhost", port=6379, db=0)
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
    await ctx.run()
