import logging
from lib.minimum_permission_level import PermissionLevel
from discord import Message


class Prompt:
    def __init__(self, schwi):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.schwi = schwi
        self.db = schwi.get_cog("Db")
        self.context = schwi.get_cog("Context")
        self.prompt = ""

    def __str__(self) -> str:
        return self.prompt

    async def add_introduction(self):
        return self.prompt  # Disabled for now.
        self.prompt += f"""
{self.schwi.user.name} is a tsundere.
"""
        users = self.db.Session.query(self.db.User).all()
        self.logger.debug(f"Users: {users}")
        for user in users:
            if user.permission_level >= PermissionLevel.TRUSTED:
                self.prompt += f"She trusts {user.name}.\n"
        self.prompt += "\n"
        return self.prompt

    async def add_chat_context(self, message, context: list[Message]):
        for message in context:
            content = message.content.replace("\n", " ")
            # Replace all mentions with their name
            for mention in message.mentions:
                content = content.replace(f"<@{mention.id}>", mention.name.lower())
                content = content.replace(f"<@!{mention.id}>", mention.name.lower())

            # If a sticker is sent, add it to the prompt
            for sticker in message.stickers:
                content += f" {sticker.name}"
            content = content.lower()

            # Global replace of all double spaces with a single space
            while "  " in content:
                content = content.replace("  ", " ")

            self.prompt += f"{message.author.name}: {content}\n"
        self.prompt += f"{self.schwi.user.name}:"

        return self.prompt
