from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class EventMetadata(BaseModel):
    event_id: UUID | str = ""
    event_type: str = ""
    created_at: datetime

    model_config = ConfigDict(extra="ignore")


class DetailImageInfoModel(BaseModel):
    bucket_id: str = ""
    object_id: str = ""

    model_config = ConfigDict(extra="ignore")


class ProductImageLoadingEvent(BaseModel):
    event_metadata: EventMetadata
    details: DetailImageInfoModel

    model_config = ConfigDict(extra="ignore")


class YandexCloudEvent(BaseModel):
    messages: list[ProductImageLoadingEvent]
    model_config = ConfigDict(extra="ignore")
