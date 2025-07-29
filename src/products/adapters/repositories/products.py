from typing import Optional
from uuid import uuid4, UUID

from sqlalchemy import Result, select, update
from sqlalchemy.orm import selectinload
from sqlalchemy.dialects.postgresql import insert

from src.core.database.interfaces.repositories import SQLAlchemyAbstractRepository
from src.core.interfaces.models import AbstractModel
from src.products.adapters.models import Product, ProductColors, ProductMaterials, ProductCategories
from src.products.domain.models import ProductMaterialAssociateModel, ProductCategoryAssociateModel
from src.products.domain.models.product import ProductModel, ProductCreateModel, ProductColorAssociateModel
from src.products.interfaces.repositories import ProductsAbstractRepository


class SQLAlchemyProductsRepository(SQLAlchemyAbstractRepository, ProductsAbstractRepository):
    async def add(self, model: ProductCreateModel) -> Optional[ProductModel]:
        product_result: Result = await self.session.execute(
            insert(Product).values(id=uuid4(), **model.model_dump(exclude={"colors", "materials", "categories"}))
            .returning(Product)
            .options(selectinload(Product.colors))
            .options(selectinload(Product.materials))
            .options(selectinload(Product.type))
            .options(selectinload(Product.collection))
            .options(selectinload(Product.categories))
        )
        product: Product = product_result.scalar_one_or_none()
        if product:
            await self.session.execute(
                insert(ProductColors).values(
                    ProductColorAssociateModel(product_ids=[product.id], color_ids=model.colors).model_associate_list()
                )
            )
            await self.session.execute(
                insert(ProductMaterials).values(
                    ProductMaterialAssociateModel(
                        product_ids=[product.id],
                        material_ids=model.materials,
                    ).model_associate_list()
                )
            )
            await self.session.execute(
                insert(ProductCategories).values(
                    ProductCategoryAssociateModel(
                        product_ids=[product.id],
                        category_ids=model.categories
                    ).model_associate_list()
                )
            )
        return ProductModel.model_validate(obj=product, from_attributes=True)

    async def get(self, id_: UUID) -> Optional[ProductModel]:
        result: Result = await self.session.execute(
            select(Product).where(Product.id == id_)
            .options(selectinload(Product.colors))
            .options(selectinload(Product.materials))
            .options(selectinload(Product.categories))
            .options(selectinload(Product.collection))
            .options(selectinload(Product.type))
            .options(selectinload(Product.images))
        )
        return self._get_domain_model_or_none(data=result, model=ProductModel)

    async def get_by_title(self, title: str) -> list[ProductModel]:
        result: Result = await self.session.execute(
            select(Product).where(Product.title == title)
        )
        if data := result.scalars().all():
            return [ProductModel.model_validate(obj=obj, from_attributes=True) for obj in data]
        return []

    async def get_list(self) -> list[ProductModel]:
        result: Result = await self.session.execute(
            select(Product).where(Product.is_active)
            .options(selectinload(Product.colors))
            .options(selectinload(Product.materials))
            .options(selectinload(Product.categories))
            .options(selectinload(Product.collection))
            .options(selectinload(Product.type))
            .options(selectinload(Product.images))
        )
        if data := result.scalars().all():
            return [ProductModel.model_validate(obj=obj, from_attributes=True) for obj in data]
        return []

    async def update(self, id_: UUID, data: dict) -> Optional[AbstractModel]:
        result: Result = await self.session.execute(
            update(Product).where(Product.id == id_).values(**data).returning(Product)
        )
        return self._get_domain_model_or_none(data=result, model=ProductModel)

    async def delete(self, id_: UUID) -> bool:
        result: Result = await self.session.execute(
            update(Product).where(Product.id == id_).values({"is_active": False}).returning(Product.id)
        )
        return True if result.scalar_one_or_none() else False
