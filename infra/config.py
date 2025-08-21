import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    discord_token: str
    database_url: str


def get_settings() -> Settings:
    return Settings(
        discord_token=os.getenv("DISCORD_TOKEN"),
        database_url=os.getenv("DATABASE_URL"),
    )
