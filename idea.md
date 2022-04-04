# Idea

## Frontends

Frontends are the components that make up the user interface. They are loaded
by the FrontendService and are responsible for passing the user input to the
CommandHandler.

### Discord

Multiple bots which can all claim a message. With 3 bots, Isla
could be asleep, so her `accepting_messages` flag is set to `False`.
Schwi and Rikka would be the only ones able to claim messages. This would
however still only be one frontend to PROJECTNAME.

### HTTP

Would buffer reply's and send them in a batch

## Services

Services are used to run things on startup and in the background. They can
also be found by calling `PROJECTNAME.services.get_service(name)`.

### Redis

Redis would be used to persist data. The reason for not using a SQL based
solution, is because SQL requires migrations and stuff, which I am not
interested in.

### CommandHandler

This service is responsible for loading and running commands.

## Commands

All commands will be run with a context object. The object's contents are
found below. The context object is passed to the command's `run` method.
Returns a translation key and a list of arguments. The translation key is
used to translate/tweak the response message.
Commands can await additional information from the user by calling the
`ctx.ask` method. This is also what the command handler uses to ask for
missing arguments.

### Homeassistant

Usage: `hass <action> <entity>`

## Classes

### BaseContext

```py
class BaseContext:
  """
  Abstract Context for all commands
  """
  def __init__(self, PROJECTNAME, message: str, author_name: str, author_mention: str):
    self.PROJECTNAME = PROJECTNAME
    self.message = message
    self.author_name = author_name
    self.author_mention = author_mention

  async def reply(self, message: str, *args, **kwargs):
    """
    Send a message to the channel the message was received in.

    Args:
      message (str): translation key for the message to send
      *args: arguments to pass to the translation
      **kwargs: keyword arguments to pass to the translation

    Returns:
      None
    """
    self.channel.send(message.format(*args, **kwargs))

  @abc.abstractmethod
  async def ask(self, message: str, *args, **kwargs) -> str:
    """
    Asks the user for follow up input

    Args:
      message (str): translation key for message to send to user
      *args: arguments to pass to message translation
      **kwargs: keyword arguments to pass to message translation

    Returns:
      str: user input
    """
    pass
```

### BaseCommand

```py
class BaseCommand:
  """
  Abstract Command
  """
  def __init__(self, PROJECTNAME):
    self.PROJECTNAME = PROJECTNAME
    self.name = "name"
    self.description = "description"
    self.aliases = ["alias"]
    self.usage = "usage"

  async def run(self, ctx: BaseContext, *args, **kwargs):
    """
    Runs the command

    Args:
      ctx (BaseContext): context object
      *args: arguments to pass to the command
      **kwargs: keyword arguments to pass to the command

    Returns:
      None
    """
    pass
```

### BaseFrontend

```py
class BaseFrontend:
  """
  Abstract Frontend
  """
  def __init__(self, PROJECTNAME):
    self.PROJECTNAME = PROJECTNAME

  async def start(self):
    """
    Makes the frontend start listening for messages

    Returns:
      None
    """
    pass
```

### BaseService

```py
class BaseService:
  """
  Abstract Service
  """
  def __init__(self, PROJECTNAME):
    self.PROJECTNAME = PROJECTNAME
    self.depends_on: list[str] = []
    """
    List of service names that this service depends on.
    """

  async def start(self):
    """
    Makes the service start running

    Returns:
      None
    """
    pass
```

### PROJECTNAME

```py
class PROJECTNAME:
  """
  PROJECTNAME
  """
  def __init__(self):
    self.services: dict[str, BaseService] = {}
    """
    Dictionary of services.
    """

  async def start(self):
    """
    Starts the PROJECTNAME

    Returns:
      None
    """
    # Load dependencies from folder, resolve dependencies
    # and start services.
    pass
```
