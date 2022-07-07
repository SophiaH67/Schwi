import logging
from lib.minimum_permission_level import PermissionLevel


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

    async def add_chat_context(self, message, context):
        for message in context:
            self.prompt += f"{message.author.name}: {message.content}\n"
        self.prompt += f"{self.schwi.user.name}:"

        return self.prompt
