from uuid import UUID

from pydantic import BaseModel

from src.core.interfaces.models import AbstractModel


class TypeCreateModel(BaseModel, AbstractModel):
    title: str


class TypeModel(TypeCreateModel):
    id: UUID


class TypeSafeModel(BaseModel):
    title: str


class TypeRelModel(TypeModel):
    product: list["ProductModel"]
