from uuid import UUID

from pydantic import BaseModel, Field, HttpUrl

from src.core.interfaces.models import AbstractModel


class ImageCreateModel(BaseModel, AbstractModel):
    title: str = Field(min_length=2, max_length=100)
    main: bool = Field(default=True)
    product_image_title_prefix: str = Field(max_length=100, min_length=2)


class ImageModel(ImageCreateModel):
    id: UUID


class ImageSafeModel(ImageCreateModel):
    main: bool
    title: str
    product_image_title_prefix: HttpUrl


class ImageRelModel(ImageModel):
    product: "ProductModel"
