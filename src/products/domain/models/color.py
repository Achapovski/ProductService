from uuid import UUID

from pydantic import BaseModel, Field

from src.core.interfaces.models import AbstractModel


class ColorCreateModel(BaseModel, AbstractModel):
    title: str = Field(min_length=3, max_length=25)


class ColorModel(ColorCreateModel):
    id: UUID


class ColorSafeModel(BaseModel):
    title: str


class ColorRelModel(ColorModel):
    products: list["ProductModel"]
