from pydantic import SecretStr, Field, PostgresDsn
from pydantic_settings import BaseSettings

from src.core.settings.schemes.base import BaseSettingsConfigMixin


class DataBaseSettings(BaseSettings, BaseSettingsConfigMixin):
    DRIVER: str
    HOST: str
    DATABASE: str
    PORT: int = Field(ge=1000, le=16394)
    USER: SecretStr
    PASSWORD: SecretStr
    IS_ECHO: bool

    @property
    def dsn(self) -> PostgresDsn:
        print(self.DATABASE)
        return PostgresDsn(
            f"{self.DRIVER}://{self.USER.get_secret_value()}:{self.PASSWORD.get_secret_value()}@{self.HOST}/{self.DATABASE}"
        )

    model_config = {
        "env_prefix": "DATABASE_",
        "extra": "ignore"
    }
