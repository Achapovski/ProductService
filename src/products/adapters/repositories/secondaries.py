from typing import Any
from uuid import UUID

from sqlalchemy import Result, delete
from sqlalchemy.dialects.postgresql import insert

from src.core.database.interfaces.repositories import SQLAlchemyAbstractRepository
from src.products.adapters.models import ProductColors
from src.products.domain.models.product import ProductColorAssociateModel


class SQLAlchemyProductsColorsAssociateRepository(SQLAlchemyAbstractRepository):
    async def add(self, model: ProductColorAssociateModel) -> bool:
        result: Result = await self.session.execute(
            insert(ProductColors).values(model.model_associate_list()).on_conflict_do_nothing()
        )
        if result.one_or_none():
            return True
        return False

    async def delete(self, id_: UUID) -> bool:
        result: Result = await self.session.execute(delete(ProductColors).where(
            ProductColors.product_id == id_ or ProductColors.color_id == id)
        )
        if result.one_or_none():
            return True
        return False

    async def get(self, id_: UUID) -> Any:
        return NotImplemented

    async def update(self, id_: UUID, data: dict) -> Any:
        return NotImplemented
