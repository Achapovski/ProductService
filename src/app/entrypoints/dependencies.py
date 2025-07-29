from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from redis.asyncio import Redis

from src.app.services.service import Service
from src.app.use_cases.product_use_case import ProductUseCase
from src.core.brokers.kafka.connection import kafka_broker
from src.core.redis.connection import redis
from src.core.settings.settings import settings
from src.infra.clients.storages import S3StorageClient
from src.products.services.service import ProductService
from src.products.services.units_of_work import SQLAlchemyProductsUnitOfWork


# Доменный слой, вызывается в products
async def get_unit_of_work() -> SQLAlchemyProductsUnitOfWork:
    return SQLAlchemyProductsUnitOfWork()


# Доменный слой, вызывается в products
async def get_product_service(
        uow: Annotated[SQLAlchemyProductsUnitOfWork, Depends(get_unit_of_work)]
) -> ProductService:
    return ProductService(uow=uow)


@lru_cache(maxsize=1)
def get_redis() -> Redis:
    return redis


async def get_storage_client() -> S3StorageClient:
    return S3StorageClient(settings=settings.S3)


async def get_product_use_case(
        product_service: Annotated[ProductService, Depends(get_product_service)],
        obj_storage: Annotated[S3StorageClient, Depends(get_storage_client)],
        key_storage: Annotated[Redis, Depends(get_redis)]

) -> ProductUseCase:
    return ProductUseCase(
        product_service=product_service,
        obj_storage=obj_storage,
        key_storage=key_storage,
        kafka=kafka_broker
    )


async def get_service() -> Service:
    uow = SQLAlchemyProductsUnitOfWork()
    product_service = ProductService(uow=uow)
    return Service(product_service=product_service, settings=settings.GRPC)
