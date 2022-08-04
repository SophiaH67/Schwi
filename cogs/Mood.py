import logging
from discord.ext import commands
import os
import requests
from lib.minimum_permission_level import is_trusted


class Mood(commands.Cog):
    def __init__(self, schwi):
        self.schwi = schwi
        self.logger = logging.getLogger(self.__class__.__name__)

    @property
    def mood(self):
        return "a bit tired"  # Static for now
