from pydantic_settings import BaseSettings, SettingsConfigDict


class RateLimit(BaseSettings):
    model_config = SettingsConfigDict(validate_default=False)

    REQUEST_PER_SECOND: int


rate_limit = RateLimit()
