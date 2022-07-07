from discord.ext import commands
import logging
from lib.minimum_permission_level import is_trusted
import docker


class Docker(commands.Cog):
    def __init__(self, schwi):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.schwi = schwi
        self.db = schwi.get_cog("Db")
        self.context = schwi.get_cog("Context")
        self.settings = schwi.get_cog("Settings")

        self.client = docker.from_env()

    @commands.group(name="docker", aliases=["d"])
    @is_trusted
    async def docker_command(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("No subcommand given.")

    @docker_command.command(name="list", aliases=["l"])
    async def docker_list(self, ctx):
        containers = self.client.containers.list(all=True)
        if len(containers) == 0:
            return await ctx.send("No containers found.")
        msg = "Containers:\n```"
        for container in containers:
            msg += f"{container.name} - {container.status}\n"
        msg += "```"
        return await ctx.send(msg)

    @docker_command.command(name="start", aliases=["s"])
    async def docker_start(self, ctx, name):
        container = self.client.containers.get(name)
        if container is None:
            return await ctx.send("Container not found.")
        if container.status == "running":
            return await ctx.send("Container is already running.")
        container.start()
        return await ctx.send(f"Started container {name}.")

    @docker_command.command(name="stop", aliases=["st"])
    async def docker_stop(self, ctx, name):
        container = self.client.containers.get(name)
        if container is None:
            return await ctx.send("Container not found.")
        if container.status != "running":
            return await ctx.send("Container is not running.")
        container.stop()
        return await ctx.send(f"Stopped container {name}.")