import asyncio
from typing import Optional
from uuid import uuid4, UUID
from ulid import ULID

from faststream.kafka import KafkaBroker
from redis.asyncio import Redis

from src.core.interfaces.storages import AbstractStorageClient
from src.products.domain.models import ImageCreateModel, ImageModel, ProductSafeModel
from src.products.domain.models.product import ProductExistsParamsModel, ProductPreCreateModel, ProductModel
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

    async def create_product(self, product: ProductPreCreateModel):
        # names = await self.obj_storage.get_objects_names(key=product_prefix)
        return await self.product_service.create_product(product=product)

    async def get_products(self) -> list[ProductSafeModel]:
        products: list[ProductModel] = await self.product_service.get_product_list()
        for product in products:
            for image in product.images:
                image.product_image_title_prefix = await self.obj_storage.object_get_url(
                    key=f"{product.image_title_prefix}/{image.title}"
                )
        return [ProductSafeModel.model_validate(obj=product, from_attributes=True) for product in products]

    async def get_product_attrs(self) -> Optional[ProductExistsParamsModel]:
        product_attrs = await self.product_service.get_product_attrs()
        return product_attrs

    async def attach_image_for_product(self, image: ImageCreateModel) -> Optional[ImageModel]:
        image = await self.product_service.create_product_image(model=image)
        return image

    async def generate_presign_urls(self, filenames: list[str]):
        prefix = uuid4()
        data = await asyncio.gather(
            *[self.obj_storage.object_post_url(key=f"{prefix}/{ULID()}.{f.split(".")[-1]}") for f in filenames]
        )
        return {"names": data, "prefix": prefix}

    async def delete_product(self, product_id: UUID):
        return await self.product_service.delete_product(id_=product_id)
