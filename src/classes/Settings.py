from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    # model_config = SettingsConfigDict(validate_default=False)

    REQUEST_PER_SECOND: int = os.getenv("REQUEST_PER_SECOND", 15)


settings = Settings()
