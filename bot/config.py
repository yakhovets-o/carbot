import os
from dataclasses import dataclass

from arq.connections import RedisSettings
from dotenv import find_dotenv, load_dotenv


load_dotenv(find_dotenv())


@dataclass
class HelpConfig:
    admin: str | None = os.getenv("ADMIN")
    support: str | None = os.getenv("SUPPORT")


@dataclass
class DatabaseConfig:
    url: str = os.getenv("URL_DB")


@dataclass
class RedisConfig:
    pool_settings = RedisSettings()


@dataclass
class BotConfig:
    token: str = os.getenv("TOKEN")
