from environs import Env
from dataclasses import dataclass

@dataclass
class Bot:
    bot_token: str
    admin_id: int

@dataclass
class Settings:
    bots: Bot

def get_settings(path: str):
    env=Env()
    env.read_env(path)

    return Settings(
        bots=Bot(
            bot_token=env.str("TOKEN"),
            admin_id=env.int("ADMIN_ID")
        )
    )

settings = get_settings('input')
print(settings)