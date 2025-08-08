import asyncio
from pathlib import Path
from typing import Optional
from uuid import uuid4, UUID
from ulid import ULID

from faststream.kafka import KafkaBroker
from redis.asyncio import Redis
from slugify import slugify

from src.core.interfaces.storages import AbstractStorageClient
from src.products.domain.models import ImageCreateModel, ImageModel, ProductSafeModel, ImagePostUrlModel, \
    ImagePreCreateModel
from src.products.domain.models.product import ProductExistsParamsModel, ProductPreCreateModel, ProductModel, \
    ProductSafeUpdateModel
from src.products.services.service import ProductService


class ProductUseCase:
    def __init__(
            self,
            kafka: KafkaBroker,
            product_service: ProductService,
            obj_storage: AbstractStorageClient,
            key_storage: Redis
    ):
        self.kafka = kafka
        self.obj_storage = obj_storage
        self.key_storage = key_storage
        self.product_service = product_service

    async def create_product(
            self,
            product: ProductPreCreateModel,
            # images: list[str]
    ) -> tuple[ProductSafeModel, ImagePostUrlModel]:

        presign_urls = await self.generate_presign_post_urls(filenames=product.images)
        created_product = await self.product_service.create_product(product=product, image_title_prefix=presign_urls.prefix)
        return ProductSafeModel(**created_product.model_dump()), presign_urls

    async def get_product(self, product_id: UUID) -> ProductSafeModel:
        product = await self.product_service.get_product(id_=product_id)
        for image in product.images:
            image.product_image_title_prefix = await self.obj_storage.object_get_url(
                key=f"{product.image_title_prefix}/{image.title}"
            )
        return ProductSafeModel(**product.model_dump())

    async def get_products(self) -> list[ProductSafeModel]:
        products: list[ProductModel] = await self.product_service.get_product_list()
        for product in products:
            for image in product.images:
                image.product_image_title_prefix = await self.obj_storage.object_get_url(
                    key=f"{product.image_title_prefix}/{image.title}"
                )
        return [ProductSafeModel.model_validate(obj=product, from_attributes=True) for product in products]

    async def update_product(self, product_id: UUID, product: ProductSafeUpdateModel) -> ProductSafeUpdateModel:
        product = await self.product_service.update_product(id_=product_id, product=product)
        return ProductSafeUpdateModel(**product.model_dump())

    async def get_product_attrs(self) -> Optional[ProductExistsParamsModel]:
        product_attrs = await self.product_service.get_product_attrs()
        return product_attrs

    async def attach_image_for_product(self, image: ImageCreateModel) -> Optional[ImageModel]:
        image = await self.product_service.create_product_image(model=image)
        return image

    async def generate_presign_post_urls(self, filenames: list[ImagePreCreateModel]) -> ImagePostUrlModel:
        prefix = uuid4()
        filenames = [slugify(Path(name.title).stem) if Path(name.title) else slugify(name.title) for name in filenames]
        images = await asyncio.gather(
            *[self.obj_storage.object_post_url(key=f"{prefix}/{ULID()}.{name}") for name in filenames]
        )
        return ImagePostUrlModel(images=images, prefix=str(prefix))

    async def delete_product(self, product_id: UUID):
        return await self.product_service.delete_product(id_=product_id)
