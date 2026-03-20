from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):

    REQUEST_PER_SECOND: int = os.getenv("REQUEST_PER_SECOND", 20)
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")


settings = Settings()
