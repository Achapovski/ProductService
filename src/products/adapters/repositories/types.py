from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import Result, select
from sqlalchemy.dialects.postgresql import insert

from src.core.database.interfaces.repositories import SQLAlchemyAbstractRepository
from src.products.adapters.models import Type
from src.products.domain.models.type import TypeCreateModel, TypeModel
from src.products.interfaces.repositories import TypesAbstractRepository


class SQLAlchemyTypesRepository(SQLAlchemyAbstractRepository, TypesAbstractRepository):
    async def add(self, model: TypeCreateModel) -> TypeModel:
        result: Result = await self.session.execute(
            insert(Type).values(
                id=uuid4(),
                **model.model_dump()
            )
            .on_conflict_do_update(
                index_elements={"title"},
                set_={"title": insert(Type).excluded.title}
            )
            .returning(Type)
        )
        return self._get_domain_model_or_none(data=result, model=TypeModel)

    async def get(self, id_: UUID) -> Optional[TypeModel]:
        result: Result = await self.session.execute(
            select(Type).where(Type.id == str(id_))
        )
        return self._get_domain_model_or_none(data=result, model=TypeModel)

    async def get_by_title(self, title: str) -> Optional[TypeModel]:
        result: Result = await self.session.execute(
            select(Type).where(Type.title == title)
        )
        return self._get_domain_model_or_none(data=result, model=TypeModel)

    async def get_list(self) -> list[TypeModel]:
        result: Result = await self.session.execute(
            select(Type)
        )
        if data := result.scalars().all():
            return [TypeModel.model_validate(obj=obj, from_attributes=True) for obj in data]
        return []

    async def update(self, id_: UUID, data: dict) -> Optional[TypeModel]:
        pass

    async def delete(self, id_: UUID) -> bool:
        pass
