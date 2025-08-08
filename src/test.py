from pydantic import BaseModel
from pydantic_settings import BaseSettings


class BaseCreateTopic(BaseModel):
    CREATE: str


class BaseDeleteTopic(BaseModel):
    DELETE: str


class UserTopics(BaseModel):
    REGISTER = "SGASHAS"
    AUTHENTICATE = "AKSSNGAIOJGASJO"


class ProductTopics(BaseModel):
    IMAGES: UserTopics


class KafkaTopics(BaseModel):
    PRODUCTS: ProductTopics
    USERS: UserTopics


class KafkaSettings(BaseSettings):
    TOPICS: KafkaTopics
