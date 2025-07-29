from decimal import Decimal
from itertools import product
from typing import Optional, ForwardRef
from uuid import UUID

from pydantic import BaseModel, Field, AnyHttpUrl, field_serializer, field_validator

from src.core.interfaces.models import AbstractModel, AssociateModel

TypeModel = ForwardRef("TypeModel")
CollectionModel = ForwardRef("CollectionModel")
ColorModel = ForwardRef("ColorModel")
CategoryModel = ForwardRef("CategoryModel")
MaterialModel = ForwardRef("MaterialModel")
CollectionSafeModel = ForwardRef("CollectionSafeModel")
TypeSafeModel = ForwardRef("TypeSafeModel")
ColorSafeModel = ForwardRef("ColorSafeModel")
MaterialSafeModel = ForwardRef("MaterialSafeModel")
CategorySafeModel = ForwardRef("CategorySafeModel")
ImageModel = ForwardRef("ImageModel")


class ProductModel(BaseModel, AbstractModel):
    id: UUID
    title: str = Field(min_length=3, max_length=45)
    description: str = Field(default="")
    price: Decimal = Field(ge=Decimal("1.0"))
    type: "TypeModel"
    collection: "CollectionModel"
    image_title_prefix: str
    discount: Decimal = Field(default=Decimal("0.0"))
    colors: list["ColorModel"]
    categories: list["CategoryModel"]
    materials: list["MaterialModel"]
    images: list["ImageModel"]

    @staticmethod
    @field_serializer("image_url")
    def serialize_url(value: AnyHttpUrl | str):
        if isinstance(value, str):
            return AnyHttpUrl(value).unicode_string()
        return value.unicode_string()

    @staticmethod
    @field_validator("image_url")
    def validate_url(value: AnyHttpUrl | str):
        if isinstance(value, str):
            return AnyHttpUrl(value).unicode_string()
        return value.unicode_string()


class ProductSafeModel(ProductModel):
    collection: "CollectionSafeModel"
    type: "TypeSafeModel"
    colors: list["ColorSafeModel"]
    materials: list["MaterialSafeModel"]
    categories: list["CategorySafeModel"]
    images: list["ImageSafeModel"]


class ProductUpdateModel(BaseModel):
    title: Optional[str] = Field(default=None, min_length=3, max_length=35)
    description: Optional[str] = Field(default=None)
    type: Optional[str] = Field(default=None, min_length=3, max_length=20)
    color: Optional[list[str]] = Field(default=None, min_length=3, max_length=20)
    price: Optional[Decimal] = Field(default=None, ge=Decimal("1.0"))
    material: Optional[list[str]] = Field(default=None, min_length=2, max_length=25)
    discount: Optional[Decimal] = Field(default=None)
    image_url: Optional[AnyHttpUrl | str] = Field(default=None)


class ProductPreCreateModel(BaseModel):
    title: str = Field(min_length=3, max_length=35)
    description: str = Field(default="")
    is_active: bool = Field(default=False)
    type: str
    collection: str
    colors: list[str] = Field(repr=False, exclude=True)
    materials: list[str] = Field(repr=False, exclude=True)
    categories: list[str] = Field(repr=False, exclude=True)
    image_title_prefix: str = Field(min_length=2, max_length=100)
    price: Decimal = Field(ge=Decimal("1.0"))
    discount: Decimal = Field(default=Decimal("0.0"))


class ProductCreateModel(BaseModel):
    title: str = Field(min_length=3, max_length=35)
    description: str = Field(default="")
    price: Decimal = Field(ge=Decimal("1.0"))
    colors: list[UUID] = Field(repr=False, exclude=True)
    type_id: UUID
    discount: Decimal = Field(default=Decimal("0.0"))
    is_active: bool = Field(default=False)
    materials: list[UUID] = Field(repr=False, exclude=True)
    categories: list[UUID] = Field(repr=False, exclude=True)
    collection_id: UUID
    image_title_prefix: str = Field(min_length=2, max_length=50)


class ProductCreateDTO(BaseModel):
    title: str = Field(min_length=3, max_length=35)
    description: str = Field(default="")
    type: str
    collection: str
    colors: list[str]
    materials: list[str]
    image_title_prefix: str
    price: Decimal = Field(ge=Decimal("1.0"))
    discount: Decimal = Field(default=Decimal("0.0"))


class ProductExistsParamsModel(BaseModel):
    types: list[str] = Field(default_factory=list)
    colors: list[str] = Field(default_factory=list)
    materials: list[str] = Field(default_factory=list)
    categories: list[str] = Field(default_factory=list)
    collections: list[str] = Field(default_factory=list)


class ProductAssociateBaseModel(BaseModel, AssociateModel):
    product_id: list[UUID] = Field(alias="product_ids")

    def model_associate_list(self) -> list[dict]:
        elements = []
        for key, value in self.model_dump().items():
            elements.append((*product((key,), value),))
        return [dict(item) for item in product(*elements)]


class ProductColorAssociateModel(ProductAssociateBaseModel):
    color_id: list[UUID] = Field(alias="color_ids")


class ProductMaterialAssociateModel(ProductAssociateBaseModel):
    material_id: list[UUID] = Field(alias="material_ids")


class ProductCategoryAssociateModel(ProductAssociateBaseModel):
    category_id: list[UUID] = Field(alias="category_ids")
