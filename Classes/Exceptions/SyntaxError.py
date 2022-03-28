from random import choice


def BotSyntaxError(Exception):
  def __str__(self):
    return choice(
      [
        "I don't understand what you want me to do.",
        "This is not enough information for me to be useful.",
      ]
    )
