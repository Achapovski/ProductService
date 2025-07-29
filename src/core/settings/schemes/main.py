from pydantic import Field
from pydantic_settings import BaseSettings


class MainSettings(BaseSettings):
    PORT: int = Field(ge=1000, le=16394)
