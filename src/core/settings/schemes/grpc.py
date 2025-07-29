from pydantic import Field
from pydantic_settings import BaseSettings


class GRPCSettings(BaseSettings):
    HOST: str
    PORT: int
    SERVER_STOP_TIMEOUT: float = Field(default=1, ge=1, le=5)

    @property
    def target_address(self):
        return f"{self.HOST}:{self.PORT}"

