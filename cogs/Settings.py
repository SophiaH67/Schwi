from discord.ext import commands
from sqlalchemy import Column, String
from lib.minimum_permission_level import is_admin


class Settings(commands.Cog):
    def __init__(self, schwi):
        self.schwi = schwi
        self.db = schwi.get_cog("Db")

        class BotSettings(self.db.Base):
            __tablename__ = "bot_setting"
            key = Column(String, primary_key=True)
            value = Column(String)

            def __init__(self, key, value):
                self.key = key
                self.value = value

        self.db.BotSettings = BotSettings

    @commands.group(name="settings")
    @is_admin
    async def settings(self, ctx):
        if ctx.invoked_subcommand is None:
            pass

    async def get_setting(self, key: str):
        setting = self.db.Session.query(self.db.BotSettings).filter_by(key=key).first()
        if setting is None:
            return None
        return setting.value

    async def get_or_create_setting(self, key: str, value: str):
        setting = self.db.Session.query(self.db.BotSettings).filter_by(key=key).first()
        if setting is None:
            setting = self.db.BotSettings(key, value)
            self.db.Session.add(setting)
            self.db.Session.commit()
        return setting.value

    async def set_setting(self, key: str, value: str):
        setting = self.db.Session.query(self.db.BotSettings).filter_by(key=key).first()
        if setting is None:
            return None
        setting.value = value
        self.db.Session.commit()
        return setting.value

    @settings.command()
    async def set(self, ctx, key, value):
        result = await self.set_setting(key, value)
        if result is None:
            return await ctx.reply("Setting not found.")
        return await ctx.reply(f"Set {key} to {value}")

    @settings.command()
    async def get(self, ctx, key=None):
        if key is None:
            settings_str = "Settings are:\n```"
            for setting in self.db.Session.query(self.db.BotSettings):
                settings_str += f"{setting.key}: {setting.value}\n"
            settings_str += "```"
            await ctx.reply(settings_str)
        else:
            value = await self.get_setting(key)
            if value is None:
                await ctx.reply(f"{key} is not set.")
            else:
                await ctx.reply(f"{key} is {value}")
