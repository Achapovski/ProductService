from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from src.products.domain.models import (ProductPreCreateModel, TypeCreateModel, ColorSafeModel, MaterialCreateModel,
                                        MaterialSafeModel, CategoryCreateModel, CategorySafeModel,
                                        CollectionCreateModel, ImageCreateModel, ImageModel)
from src.products.domain.models.color import ColorCreateModel, ColorModel
from src.products.domain.models.product import (ProductModel, ProductCreateModel,
                                                ProductSafeUpdateModel, ProductExistsParamsModel, ProductUpdateModel)
from src.products.exceptions.exceptions import ProductAlreadyExistsException, ProductNotFoundException
from src.products.interfaces.units_of_work import ProductUnitOfWork


class ProductService:
    def __init__(self, uow: ProductUnitOfWork):
        self._uow: ProductUnitOfWork = uow

    async def create_product(self, product: ProductPreCreateModel, image_title_prefix: str) -> ProductModel:
        async with self._uow as uow:
            colors = await self.add_colors(colors_list=product.colors, uow=uow)
            materials = await self.add_materials(materials_list=product.materials, uow=uow)
            categories = await self.add_categories(categories_list=product.categories, uow=uow)
            type_ = await uow.types.add(model=TypeCreateModel(title=product.type))
            collection = await uow.collections.add(model=CollectionCreateModel(title=product.title))
            model = ProductCreateModel(
                materials=[material.id for material in materials],
                colors=[color.id for color in colors],
                categories=[category.id for category in categories],
                type_id=type_.id,
                collection_id=collection.id,
                image_title_prefix=image_title_prefix,
                **product.model_dump())
            product: ProductModel = await uow.products.add(model=model)
            if product:
                product.colors.extend(
                    [ColorSafeModel.model_validate(obj=obj, from_attributes=True) for obj in colors])
                product.materials.extend(
                    [MaterialSafeModel.model_validate(obj=obj, from_attributes=True) for obj in materials]
                )
                product.categories.extend(
                    [CategorySafeModel.model_validate(obj=obj, from_attributes=True) for obj in categories]
                )
            else:
                raise ProductAlreadyExistsException()
            await uow.commit()
            return product

    async def update_product(self, id_: UUID, product: ProductSafeUpdateModel) -> Optional[ProductModel]:
        async with self._uow as uow:
            if product.model_dump(exclude_none=True, exclude_unset=True, exclude_defaults=True):
                colors = await self.add_colors(
                    colors_list=product.colors,
                    uow=uow
                ) if product.colors else []
                materials = await self.add_materials(
                    materials_list=product.materials,
                    uow=uow
                ) if product.materials else []
                categories = await self.add_categories(
                    categories_list=product.categories,
                    uow=uow
                ) if product.categories else []
                type_ = await uow.types.add(model=TypeCreateModel(title=product.type))
                collection = await uow.collections.add(model=CollectionCreateModel(title=product.title))
                product_update_model = ProductUpdateModel(
                    colors=colors,
                    materials=materials,
                    categories=categories,
                    type=type_,
                    collection=collection,
                    **product.model_dump(exclude={"type", "collection", "colors", "materials", "categories"})
                )
                product = await uow.products.update(id_=id_, model=product_update_model)
            if product:
                await uow.commit()
                return product
            raise ProductNotFoundException()

    async def add_colors(
            self,
            colors_list: list[ColorSafeModel | str],
            uow: ProductUnitOfWork = None
    ) -> list[ColorModel]:
        model_list = [ColorCreateModel(title=color if isinstance(color, str) else color.title) for color in colors_list]
        if not uow:
            async with self._uow as uow:
                return await uow.colors.add_many(model_list=model_list)
        return await uow.colors.add_many(model_list=model_list)

    async def add_materials(self, materials_list: list[MaterialSafeModel | str], uow: ProductUnitOfWork = None):
        model_list = [MaterialCreateModel(title=material if type(material) is str else material.title) for material in
                      materials_list]
        if not uow:
            async with self._uow as uow:
                return await uow.materials.add_many(model_list=model_list)
        return await uow.materials.add_many(model_list=model_list)

    async def add_categories(self, categories_list: list[CategorySafeModel | str], uow: ProductUnitOfWork = None):
        model_list = [CategoryCreateModel(title=category if type(category) is str else category.title) for category in
                      categories_list]
        if not uow:
            async with self._uow as uow:
                return await uow.categories.add_many(model_list=model_list)
        return await uow.categories.add_many(model_list=model_list)

    async def get_product(self, id_: UUID) -> Optional[ProductModel]:
        async with self._uow as uow:
            if not (product := await uow.products.get(id_=id_)):
                raise ProductNotFoundException()
        return product

    async def create_product_image(self, model: ImageCreateModel) -> ImageModel:
        async with self._uow as uow:
            image = await uow.images.add(model=model)
            await uow.commit()
        return image

    async def get_colors(self):
        async with self._uow as uow:
            colors = await uow.colors.get_list()
        return colors

    async def get_product_attrs(self) -> Optional[ProductExistsParamsModel]:
        def title_map(data: list[BaseModel]) -> list[str]:
            return [item.title for item in data]

        async with self._uow as uow:
            product_config_model = ProductExistsParamsModel(
                colors=title_map(await uow.colors.get_list()),
                materials=title_map(await uow.materials.get_list()),
                types=title_map(await uow.types.get_list()),
                categories=title_map(await uow.categories.get_list()),
                collections=title_map(await uow.collections.get_list()),
            )
        return product_config_model

    async def get_product_list(self) -> list[ProductModel]:
        async with self._uow as uow:
            products = await uow.products.get_list()
        return products

    async def delete_product(self, id_: UUID) -> bool:
        async with self._uow as uow:
            result = await uow.products.delete(id_=id_)
            await uow.commit()
        return result
