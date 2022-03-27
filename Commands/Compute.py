from Classes.BaseCommand import BaseCommand
from Classes.MessageContext import MessageContext
import openai
import os

openai.api_key = os.getenv("OPENAI_KEY")


class Command(BaseCommand):
  aliases = ["compute", "what", "who", "why", "when", "where", "how"]

  async def run(self, ctx: MessageContext):
    prompt = ctx.message.content
    if ctx.command == "compute":
      prompt = prompt[len("compute ") :]
    completion = openai.Completion.create(
      engine="text-davinci-002", prompt=prompt, max_tokens=64
    )
    text: str = completion.choices[0].text
    text = text.strip()
    await ctx.success(text)
