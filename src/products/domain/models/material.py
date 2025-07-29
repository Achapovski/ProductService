from uuid import UUID

from pydantic import BaseModel

from src.core.interfaces.models import AbstractModel


class MaterialCreateModel(BaseModel, AbstractModel):
    title: str


class MaterialModel(MaterialCreateModel):
    id: UUID


class MaterialSafeModel(BaseModel):
    title: str


class ImageRelModel(MaterialModel):
    product: list["ProductModel"]
