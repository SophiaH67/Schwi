from typing import List
from discord.ext import commands
import logging
from discord import Message


class ListWithMaxLength(list):
    def __init__(self, max_length: int):
        self.max_length = max_length
        super().__init__()

    def append(self, item):
        if len(self) >= self.max_length:
            self.pop(0)
        super().append(item)


class Context(commands.Cog):
    def __init__(self, schwi):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.schwi = schwi
        self.context = {}

    def get_context(self, channel_id) -> List[Message]:
        if channel_id not in self.context:
            self.context[channel_id] = ListWithMaxLength(10)
        return self.context[channel_id]

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content == "##compute##":
            return
        if not message.channel.id in self.context:
            self.context[message.channel.id] = ListWithMaxLength(10)
        context_list = self.context[message.channel.id]
        if len(context_list) > 0:
            last_message = context_list[-1]
            if last_message.author == message.author:
                last_message.content += f"\n{message.content}"
        else:
            context_list.append(message)
