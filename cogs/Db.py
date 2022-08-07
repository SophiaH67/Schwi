from discord.ext import commands
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from lib.minimum_permission_level import is_admin
import os

from schwi.SchwiCog import SchwiCog


class Db(SchwiCog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.engine = create_engine(os.environ["DATABASE_URL"])
        self.Base = declarative_base()
        self.SessionMaker = sessionmaker(bind=self.engine)
        self.Session = self.SessionMaker()

        class BotSettings(self.Base):
            __tablename__ = "bot_settings"
            key = Column(String, primary_key=True)
            value = Column(String)

        self.BotSettings = BotSettings

    @commands.command(name="migrate")
    @is_admin
    async def migrate(self, ctx):
        self.Base.metadata.create_all(self.engine)
        await ctx.reply("Migration complete.")

    @commands.Cog.listener()
    async def on_ready(self):
        self.Base.metadata.create_all(self.engine)
        self.logger.info("Database migrated.")
