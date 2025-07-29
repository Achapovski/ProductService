from decimal import Decimal
from email.policy import default
from uuid import UUID

from pydantic import BaseModel, Field

from src.core.interfaces.models import AbstractModel


class CollectionCreateModel(BaseModel, AbstractModel):
    title: str
    is_active: bool = Field(default=False)
    description: str = Field(default="")
    discount: Decimal = Field(default=Decimal("0.0"))


class CollectionModel(CollectionCreateModel):
    id: UUID


class CollectionSafeModel(BaseModel):
    title: str
    description: str
    discount: Decimal


class CollectionSafeRelModel(CollectionSafeModel):
    product: list["ProductModel"]


class CollectionRelModel(CollectionModel):
    product: list["ProductModel"]
