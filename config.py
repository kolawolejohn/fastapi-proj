from pydantic import ConfigDict
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    DB_NAME: str
    DB_USERNAME: str
    DB_PASSWORD: str
    SECRET_KEY: str
    # class Config:
    #     env_file: str = ".env"
    model_config = ConfigDict(env_file=".env")


def get_settings() -> Settings:
    return Settings()
