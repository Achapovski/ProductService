from pydantic import BaseModel
from pydantic_settings import BaseSettings


class BaseCreateTopic(BaseModel):
    CREATE: str


class BaseDeleteTopic(BaseModel):
    DELETE: str


class UserTopics(BaseModel):
    REGISTER: str
    AUTHENTICATE: str


class ImageTopics(BaseModel):
    CREATE: str
    DELETE: str


class ProductTopics(BaseModel):
    IMAGES: ImageTopics


class KafkaTopics(BaseModel):
    PRODUCTS: ProductTopics
    USERS: UserTopics


class KafkaSettings(BaseSettings):
    BOOSTRAP_SERVERS: list[str]
    TOPICS: KafkaTopics
