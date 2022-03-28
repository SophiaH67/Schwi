from random import choice


def PermissionsException(Exception):
  def __str__(self):
    return choice(
      [
        "You lack the permissions to use this command.",
        "Schwi can't do that for you.",
      ]
    )
