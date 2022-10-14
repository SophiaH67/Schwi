from typing import TYPE_CHECKING
from discord.ext import commands
import logging
from sqlalchemy.orm.decl_api import DeclarativeMeta
from asyncio import sleep


if TYPE_CHECKING:
    from ..main import Schwi


class SchwiCog(commands.Cog):
    dependencies: list[str] = []
    models: list[callable] = []
    tick: callable or None = None
    tick_delay = 10

    def __init__(self, schwi: "Schwi"):
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
                try:
                    await self.tick()
                except Exception as e:
                    self.logger.error(e, exc_info=True)
            await sleep(self.tick_delay)
