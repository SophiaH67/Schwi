from discord.ext import commands
import logging


class SchwiCog(commands.Cog):
    dependencies: list[str] = []

    def __init__(self, schwi):
        self.schwi = schwi
        self.logger = logging.getLogger(self.__class__.__name__)

        for dependency in self.dependencies:
            setattr(self, dependency.lower(), schwi.get_cog(dependency))
