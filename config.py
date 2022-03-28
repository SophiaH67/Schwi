import os

redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = os.getenv("REDIS_PORT", 6379)
discord_token = os.getenv("DISCORD_TOKEN")
openai_key = os.getenv("OPENAI_KEY")

assert discord_token is not None
assert openai_key is not None
