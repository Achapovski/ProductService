from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from src.products.domain.models import ProductPreCreateModel, TypeCreateModel, ProductSafeModel, ColorSafeModel, \
    MaterialCreateModel, MaterialSafeModel, CategoryCreateModel, CategorySafeModel, CollectionCreateModel, \
    ImageCreateModel, ImageModel
from src.products.domain.models.color import ColorCreateModel
from src.products.domain.models.product import ProductModel, ProductCreateModel, ProductUpdateModel, \
    ProductExistsParamsModel
from src.products.interfaces.units_of_work import ProductUnitOfWork


class ProductService:
    def __init__(self, uow: ProductUnitOfWork):
        self._uow: ProductUnitOfWork = uow

    async def create_product(self, product: ProductPreCreateModel) -> Optional[ProductModel]:
        async with self._uow as uow:
            colors = await uow.colors.add_many(
                model_list=[ColorCreateModel(title=color) for color in product.colors]
            )
            materials = await uow.materials.add_many(
                model_list=[MaterialCreateModel(title=material) for material in product.materials]
            )
            categories = await uow.categories.add_many(
                model_list=[CategoryCreateModel(title=category) for category in product.categories]
            )
            type_ = await uow.types.add(model=TypeCreateModel(title=product.type))
            collection = await uow.collections.add(model=CollectionCreateModel(title=product.title))
            model = ProductCreateModel(
                materials=[material.id for material in materials],
                colors=[color.id for color in colors],
                categories=[category.id for category in categories],
                type_id=type_.id,
                collection_id=collection.id,
                **product.model_dump())
            product: ProductModel = await uow.products.add(model=model)
            product.colors.extend(
                [ColorSafeModel.model_validate(obj=obj, from_attributes=True) for obj in colors])
            product.materials.extend(
                [MaterialSafeModel.model_validate(obj=obj, from_attributes=True) for obj in materials]
            )
            product.categories.extend(
                [CategorySafeModel.model_validate(obj=obj, from_attributes=True) for obj in categories]
            )
            await uow.commit()
        return ProductSafeModel.model_validate(obj=product, from_attributes=True)

    async def update_product(self, id_: UUID, product: ProductUpdateModel) -> Optional[ProductModel]:
        async with self._uow as uow:
            if clean_model := product.model_dump(exclude_none=True, exclude_unset=True, exclude_defaults=True):
                product = await uow.products.update(id_=id_, data=clean_model)
                await uow.commit()
        return product

    async def get_product(self, id_: UUID) -> Optional[ProductModel]:
        async with self._uow as uow:
            product = await uow.products.get(id_=id_)
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
