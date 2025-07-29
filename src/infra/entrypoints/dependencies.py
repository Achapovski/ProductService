from functools import lru_cache
from typing import Annotated

from fast_depends import Depends
from redis.asyncio import Redis

from src.app.entrypoints.dependencies import get_storage_client, get_redis
from src.app.use_cases.product_use_case import ProductUseCase
from src.core.brokers.kafka.connection import kafka_broker
from src.infra.clients.storages import S3StorageClient
from src.products.services.service import ProductService
from src.products.services.units_of_work import SQLAlchemyProductsUnitOfWork


async def get_product_use_case(
        key_storage: Annotated[Redis, Depends(get_redis)],
        obj_storage: Annotated[S3StorageClient, Depends(get_storage_client)]
) -> ProductUseCase:
    uow = SQLAlchemyProductsUnitOfWork()
    product_service = ProductService(uow=uow)

    return ProductUseCase(
        product_service=product_service,
        obj_storage=obj_storage,
        key_storage=key_storage,
        kafka=kafka_broker
    )
