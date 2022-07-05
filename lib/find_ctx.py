from discord.ext import commands

class ContextNotFoundException(Exception):
    pass


def find_ctx(*args) -> commands.Context:
    for arg in args:
        if isinstance(arg, commands.Context):
            return arg
    raise ContextNotFoundException()