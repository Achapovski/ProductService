from pydantic_settings import BaseSettings

from src.core.settings.schemes.base import BaseSettingsConfigMixin


class S3Settings(BaseSettings, BaseSettingsConfigMixin):
    BUCKET: str
    ENDPOINT_URL: str
    SERVICE_NAME: str
    ACCESS_KEY_ID: str
    SECRET_ACCESS_KEY: str

    model_config = {
        "env_prefix": "AWS_",
        "extra": "ignore"
    }
