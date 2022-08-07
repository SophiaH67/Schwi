from heapq import heappop
from lib.FadingFloat import FadingFloat
from schwi.SchwiCog import SchwiCog
from discord.ext import commands
import arrow
from random import random
from discord import Status, Game


class Mood(SchwiCog):
    asleep = False

    # frustration is affected by both command errors and completions
    frustration = FadingFloat(0.5, 60 * 60)
    # exhaustion is affected by number of messages schwi has sent
    exhaustion = 0

    @commands.Cog.listener()
    async def on_command_error(self, ctx, err):
        self.frustration += 0.1 * random()

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        self.frustration += -0.1 * random()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == self.schwi.user.id:
            self.exhaustion += 0.1 * random()

    async def tick(self):
        # Add randomness to the mood
        self.frustration += 0.1 * (0.5 - random())
        exhaustion_change = 0.0025 * (0.5 + (random() / 2))
        if self.asleep:
            self.exhaustion -= exhaustion_change * 2
        else:
            self.exhaustion += exhaustion_change
        # Check if the bot is asleep
        if self.exhaustion > 0.8 and not self.asleep:
            if random() < 0.1:
                self.asleep = True
        if self.asleep and self.exhaustion < 0.2:
            if random() < 0.1:
                self.asleep = False

        self.logger.debug(
            f"state: {self.mood} | exhaustion: {self.exhaustion} | frustration: {self.frustration}"
        )
        # Update discord status
        status = Status.online
        if self.asleep:
            status = Status.idle
        elif self.frustration > 0.7:
            status = Status.dnd
        game = Game(name=f"{self.mood}")
        await self.schwi.change_presence(status=status, activity=game)

    @property
    def mood(self) -> str:
        states = []
        if self.asleep:
            states.append("asleep")
        if self.frustration > 0.7:
            states.append("frustrated")
        if self.exhaustion > 0.7:
            states.append("exhausted")
        if len(states) == 0:
            return "calm"
        # Return in human readable format
        return " & ".join(", ".join(states).rsplit(", ", 1))
