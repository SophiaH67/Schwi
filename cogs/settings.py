from discord.ext import commands


class Settings(commands.Cog):
    def __init__(self, schwi):
        self.schwi = schwi
        self.settings = {
            "key": "value",
            "key2": "value2",
        }

    @commands.group()
    async def settings(self, ctx):
        if ctx.invoked_subcommand is None:
            pass

    @settings.command()
    async def set(self, ctx, key, value):
        if key in self.settings:
            self.settings[key] = value
            await ctx.send("Setting changed.")
        else:
            await ctx.send("Setting not found.")

    @settings.command()
    async def get(self, ctx, key=None):
        if key is None:
            settings_str = "Settings are:\n```"
            for key, value in self.settings.items():
                settings_str += f"{key}: {value}\n"
            settings_str += "```"
            await ctx.send(settings_str)
        elif key in self.settings:
            await ctx.send(self.settings[key])
        else:
            await ctx.send("Setting not found.")
