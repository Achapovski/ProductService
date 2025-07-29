from uuid import UUID

from pydantic import BaseModel

from src.core.interfaces.models import AbstractModel


class CategoryCreateModel(BaseModel, AbstractModel):
    title: str


class CategoryModel(CategoryCreateModel):
    id: UUID


class CategorySafeModel(BaseModel):
    title: str


class CategoryRelModel(CategoryModel):
    product: list["ProductModel"]
