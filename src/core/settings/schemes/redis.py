from pydantic import Field, RedisDsn
from pydantic_settings import BaseSettings


class RedisSettings(BaseSettings):
    CONNECTION: str
    HOST: str
    PORT: int = Field(ge=1000, le=16394)
    DB_NUMBER: int = Field(ge=0, le=15)

    def dsn(self, db_number: Field(ge=0, le=15) = 0):
        return RedisDsn(
            f"{self.CONNECTION}://{self.HOST}:{self.PORT}/{db_number}"
        )
