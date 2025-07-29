from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import Result, select
from sqlalchemy.dialects.postgresql import insert

from src.core.database.interfaces.repositories import SQLAlchemyAbstractRepository
from src.products.adapters.models import Material
from src.products.domain.models.material import MaterialCreateModel, MaterialModel
from src.products.domain.models.product import ProductModel
from src.products.interfaces.repositories import MaterialsAbstractRepository


class SQLAlchemyMaterialsRepository(SQLAlchemyAbstractRepository, MaterialsAbstractRepository):
    async def add(self, model: MaterialCreateModel) -> MaterialModel:
        pass

    async def add_many(self, model_list: list[MaterialCreateModel]) -> list[MaterialModel]:
        result: Result = await self.session.execute(
            insert(Material).values(
                [{"id": uuid4(), "title": color.title} for color in model_list]
            ).on_conflict_do_update(
                index_elements={"title"},
                set_={"title": insert(Material).excluded.title}
            ).returning(Material)
        )
        if data := result.scalars().all():
            return [MaterialModel.model_validate(obj=obj, from_attributes=True) for obj in data]
        return []

    async def get(self, id_: UUID) -> Optional[MaterialModel]:
        result: Result = await self.session.execute(
            select(Material).where(Material.id == str(id_))
        )
        return self._get_domain_model_or_none(data=result, model=MaterialModel)

    async def get_by_title(self, title: str) -> Optional[MaterialModel]:
        result: Result = await self.session.execute(
            select(Material).where(Material.title == title)
        )
        return self._get_domain_model_or_none(data=result, model=MaterialModel)

    async def get_list(self) -> list[MaterialModel]:
        result: Result = await self.session.execute(
            select(Material)
        )
        if data := result.scalars().all():
            return [MaterialModel.model_validate(obj=obj, from_attributes=True) for obj in data]
        return []

    async def update(self, id_: UUID, data: dict) -> Optional[ProductModel]:
        pass

    async def delete(self, id_: UUID) -> bool:
        pass
