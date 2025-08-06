from typing import Optional
from uuid import uuid4, UUID

from sqlalchemy import Result, select, update, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.dialects.postgresql import insert

from src.core.database.interfaces.repositories import SQLAlchemyAbstractRepository
from src.products.adapters.models import Product, ProductColors, ProductMaterials, ProductCategories
from src.products.domain.models import ProductMaterialAssociateModel, ProductCategoryAssociateModel, ProductSafeUpdateModel
from src.products.domain.models.product import ProductModel, ProductCreateModel, ProductColorAssociateModel, \
    ProductUpdateModel
from src.products.interfaces.repositories import ProductsAbstractRepository


class SQLAlchemyProductsRepository(SQLAlchemyAbstractRepository, ProductsAbstractRepository):
    async def add(self, model: ProductCreateModel) -> Optional[ProductModel]:
        product_result: Result = await self.session.execute(
            insert(Product).values(id=uuid4(), **model.model_dump(exclude={"colors", "materials", "categories"}))
            .on_conflict_do_nothing()
            .returning(Product)
            .options(selectinload(Product.colors))
            .options(selectinload(Product.materials))
            .options(selectinload(Product.type))
            .options(selectinload(Product.collection))
            .options(selectinload(Product.categories))
            .options(selectinload(Product.images))
        )
        product = self._get_domain_model_or_none(data=product_result, model=ProductModel)
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
        return product

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

    async def update(self, id_: UUID, model: ProductUpdateModel) -> Optional[ProductModel]:
        result: Result = await self.session.execute(
            update(Product).where(Product.id == id_).values(
                **model.model_dump(exclude={"colors", "materials", "categories"})
            ).returning(Product)
            .options(selectinload(Product.colors))
            .options(selectinload(Product.materials))
            .options(selectinload(Product.categories))
            .options(selectinload(Product.collection))
            .options(selectinload(Product.type))
            .options(selectinload(Product.images))
        )
        product = self._get_domain_model_or_none(data=result, model=ProductModel)
        if product:
            if model.colors:
                await self.session.execute(
                    delete(ProductColors).where(ProductColors.product_id == product.id)
                )
                await self.session.execute(
                    insert(ProductColors).values(
                        ProductColorAssociateModel(
                            product_ids=[product.id],
                            color_ids=[color.id for color in model.colors]
                        ).model_associate_list()))
            if model.materials:
                await self.session.execute(
                    delete(ProductMaterials).where(ProductMaterials.product_id == product.id)
                )
                await self.session.execute(
                    insert(ProductMaterials).values(
                        ProductMaterialAssociateModel(
                            product_ids=[product.id],
                            material_ids=[material.id for material in model.materials]
                        ).model_associate_list()))
            if model.categories:
                await self.session.execute(
                    delete(ProductCategories).where(ProductCategories.product_id == product.id)
                )
                await self.session.execute(
                    insert(ProductCategories).values(
                        ProductCategoryAssociateModel(
                            product_ids=[product.id],
                            category_ids=[category.id for category in model.categories]
                        ).model_associate_list()))

            product = await self.get(id_=id_)
        return product

    async def delete(self, id_: UUID) -> bool:
        result: Result = await self.session.execute(
            update(Product).where(Product.id == id_).values({"is_active": False}).returning(Product.id)
        )
        return True if result.scalar_one_or_none() else False
