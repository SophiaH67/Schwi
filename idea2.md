# Idea2

## Frontends

The general bot has multiple frontends. Frontends are responsible for sending Context's to the command handler and
handling the data returned from the command handler.

An example return string is `Isla: Turned on the lights, bakaa` or `Schwi: Success: Lights are now off.`.

A frontend can choose to display these messages in a specific way. For example, the Discord frontend will use a
different discord user for each different personality.

## Services

Services are used to run things on startup and in the background. They can also be found by calling
`Schwi.services.get_service(name)`. Which returns a handle to the service. A service is a class that implements
the `Service` interface described below in the `Classes` section.

### CommandHandler

The command handler is responsible for loading and running commands. It is also responsible for handling the
data returned from the command, and passing it through a personality before returning it to the frontend that
called the command.

## Personalities

The PersonalityService is responsible for loading and running personalities. It can be given a translation key
and a list of arguments for the personality to react to.

Each personality has a name, a description and a boolean flag to indicate if it is accepting messages(Would be
set to `False` if the personality is sleeping).

### Isla

This personality uses GPT-3 to change its sentences. It is supposed to somewhat resemble the Isla from the
anime Plastic Memories.

### Rikka

This personality also uses GPT-3 to change its sentences. It is supposed to resemble the Rikka from the
anime Chuunibyou demo Koi ga Shitai. (I like chuunibyous)

### Schwi

In contrast, Schwi uses a preset list of sentences and prefixes messages with return type. Such as `Success:`,
`Error:`, etc.

## Classes

```py
class BaseContext:
  """
  Abstract Context for all commands
  """
  def __init__(self, schwi, message: str, author_name: str, author_mention: str):
    self.schwi = schwi
    self.message = message
    self.author_name = author_name
    self.author_mention = author_mention
```

```py
class BaseService:
  """
  Abstract Service
  """
  def __init__(self, schwi):
    self.schwi = schwi

  async def start(self):
    """
    Called when the service is started
    """
    pass
```

```py
class BasePersonality:
  """
  Abstract Personality
  """
  def __init__(self, schwi, name: str, description: str):
    self.schwi = schwi
    self.name = name
    self.description = description
    self.accepting_messages = True

  def start(self):
    """
    Called when the personality is started
    """
    pass

  async def react(self, translation_key: str, *args, **kwargs):
    """
    Called when the personality is reacting to a message
    """
    pass
```
