import logging
from discord.ext import commands
import nltk
import openai
import numpy

nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")
nltk.download("words")
nltk.download("wordnet")
nltk.download("stopwords")


class NaturalLanguage(commands.Cog):
    def __init__(self, schwi):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.schwi = schwi
        self.context = schwi.get_cog("Context")
        self.settings = schwi.get_cog("Settings")

        self.answer_on = ["WRB", "$WP", "WP", "WDT", "MD"]

    @property
    async def engine(self):
        return await self.settings.get_or_create_setting(
            "natural_language_engine", "text-davinci-002"
        )

    @property
    async def temperature(self):
        return await self.settings.get_or_create_setting(
            "natural_language_temperature", "0.8"
        )

    @property
    async def max_length(self):
        return await self.settings.get_or_create_setting(
            "natural_language_max_length", "64"
        )

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.schwi.user:
            self.logger.debug("Not answering to myself.")
            return
        tokens = nltk.word_tokenize(message.content)
        tagged = nltk.pos_tag(tokens)

        answer = False
        for token in tagged:
            if token[1] in self.answer_on:
                answer = True
                break

        if answer:
            await self.answer_message(message)
        else:
            self.logger.debug(f"Not answering {message.content} ({str(tagged)})")

    async def answer_message(self, message):
        context = self.context.get_context(message.channel.id)
        prompt = """
Schwi is a character who does not like talking to people she doesn't know.
She is friends with Marnix, who likes computers and anime.

"""  # Last part needs to be done automatically.
        for message in context:
            prompt += f"{message.author.name}: {message.content}\n"
        prompt += "Schwi:"

        # So that GPT doesn't generate stuff for other people
        recent_unique_authors = list(map(lambda message: message.author, context))
        self.logger.debug(f"Recent unique authors: {recent_unique_authors}")

        [recent_unique_authors, indexes] = numpy.unique(
            recent_unique_authors, return_index=True
        )
        recent_unique_authors = [
            recent_unique_authors[index] for index in sorted(indexes)
        ]
        recent_unique_authors = list(recent_unique_authors)
        self.logger.debug(f"Recent unique authors: {recent_unique_authors}")
        stop_tokens = []
        for recent_unique_author in recent_unique_authors[::-1]:
            stop_tokens.append(f"{recent_unique_author.name}:")
            if len(stop_tokens) > 2:
                break

        response = (
            openai.Completion.create(
                engine=await self.engine,
                prompt=prompt,
                temperature=float(await self.temperature),
                max_tokens=int(await self.max_length),
                stop=stop_tokens,
            )
            .choices[0]
            .text
        )
        await message.channel.send(response)
