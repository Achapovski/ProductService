from pydantic import BaseModel
from pydantic_settings import BaseSettings


class UserTopics(BaseModel):
    REGISTER: str
    AUTHENTICATE: str


class KafkaTopics(BaseModel):
    USERS: UserTopics


class KafkaSettings(BaseSettings):
    BOOSTRAP_SERVERS: list[str]
    # TOPICS: KafkaTopics
