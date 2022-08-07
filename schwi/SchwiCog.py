from discord.ext import commands
import logging
from sqlalchemy.orm.decl_api import DeclarativeMeta
from asyncio import sleep


class SchwiCog(commands.Cog):
    dependencies: list[str] = []
    models: list[callable] = []
    tick: callable or None = None
    tick_delay = 10

    def __init__(self, schwi):
        self.schwi = schwi
        self.logger = logging.getLogger(self.__class__.__name__)

        if len(self.models) > 0 and not "Db" in self.dependencies:
            self.dependencies.append("Db")

        for dependency in self.dependencies:
            setattr(self, dependency.lower(), schwi.get_cog(dependency))

        for model_factory in self.models:
            base: DeclarativeMeta = self.db.Base
            model = model_factory(base)
            setattr(self.db, model.__name__, model)

        if self.tick is not None:
            self.schwi.loop.create_task(self.tick_loop())

    async def tick_loop(self):
        while True:
            if self.schwi.user:  # In case the bot is not logged in
                await self.tick()
            await sleep(self.tick_delay)
