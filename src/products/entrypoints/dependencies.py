from typing import Annotated

from fastapi import Depends

from src.products.services.service import ProductService
from src.products.services.units_of_work import SQLAlchemyProductsUnitOfWork


async def get_users_unit_of_work() -> SQLAlchemyProductsUnitOfWork:
    return SQLAlchemyProductsUnitOfWork()


async def get_user_service(
        uow: Annotated[SQLAlchemyProductsUnitOfWork, Depends(get_users_unit_of_work)]
) -> ProductService:
    return ProductService(uow=uow)
