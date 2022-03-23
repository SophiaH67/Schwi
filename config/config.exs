import Config

config :nostrum,
  # The token of your bot as a string(env)
  token: System.get_env("DISCORD_TOKEN"),
  gateway_intents: [
    :guilds,
    :message_content,
    :direct_messages
  ]

config :logger,
  # The log level of the logger as a string(env)
  level: :info
