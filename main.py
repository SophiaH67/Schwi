from dotenv import load_dotenv

load_dotenv()

import config
from Classes.Schwi import Schwi

schwi = Schwi()


schwi.run(config.discord_token)
