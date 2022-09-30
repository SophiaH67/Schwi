from typing import List
from discord.ext import commands
from discord import Message
from transformers import GPT2TokenizerFast

from schwi.SchwiCog import SchwiCog


class ListWithMaxLength(list):
    def __init__(self, max_length: int):
        self.max_length = max_length
        super().__init__()

    def append(self, item):
        if len(self) >= self.max_length:
            self.pop(0)
        super().append(item)


class Context(SchwiCog):
    dependencies = ["Settings"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.context = {}
        self.tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")

    def get_context(self, channel_id) -> List[Message]:
        if channel_id not in self.context:
            self.context[channel_id] = ListWithMaxLength(5)
        return self.context[channel_id]

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content == "##compute##":
            return
        if not message.channel.id in self.context:
            self.context[message.channel.id] = ListWithMaxLength(5)
        self.logger.debug(
            f"List for channel {message.channel.id}: {self.context[message.channel.id]}"
        )
        context_list = self.context[message.channel.id]
        context_list.append(message)
