from Classes.Schwi import Schwi
import os

schwi = Schwi()

@schwi.event
async def on_ready():
  print(f"Schwi is ready as {schwi.user}")

@schwi.event
async def on_message(message):
  if message.author == Schwi.user:
    return
  print(f"{message.author}: {message.content}")

schwi.run(os.environ['DISCORD_TOKEN'])
