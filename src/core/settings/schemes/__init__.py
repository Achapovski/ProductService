from pydantic import BaseModel, ConfigDict

from src.core.settings.schemes.database import DataBaseSettings
from src.core.settings.schemes.grpc import GRPCSettings
from src.core.settings.schemes.broker import KafkaSettings
from src.core.settings.schemes.main import MainSettings
from src.core.settings.schemes.redis import RedisSettings
from src.core.settings.schemes.storage import S3Settings


class Settings(BaseModel):
    S3: S3Settings
    MAIN: MainSettings
    GRPC: GRPCSettings
    REDIS: RedisSettings
    KAFKA: KafkaSettings
    DATABASE: DataBaseSettings

    model_config = ConfigDict(extra="ignore")


__all__ = ["Settings"]
