from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import Result, select
from sqlalchemy.dialects.postgresql import insert

from src.core.database.interfaces.repositories import SQLAlchemyAbstractRepository
from src.products.adapters.models import Collection
from src.products.domain.models.collection import CollectionCreateModel, CollectionModel
from src.products.interfaces.repositories import CollectionsAbstractRepository


class SQLAlchemyCollectionsRepository(SQLAlchemyAbstractRepository, CollectionsAbstractRepository):
    async def add(self, model: CollectionCreateModel) -> CollectionModel:
        result: Result = await self.session.execute(
            insert(Collection).values(
                id=uuid4(),
                **model.model_dump()
            )
            .on_conflict_do_update(
                index_elements={"title"},
                set_={"title": insert(Collection).excluded.title}
            )
            .returning(Collection)
        )
        return self._get_domain_model_or_none(data=result, model=CollectionModel)

    async def get(self, id_: UUID) -> Optional[CollectionModel]:
        result: Result = await self.session.execute(
            select(Collection).where(Collection.id == str(id_))
        )
        return self._get_domain_model_or_none(data=result, model=CollectionModel)

    async def get_by_title(self, title: str) -> Optional[CollectionModel]:
        result: Result = await self.session.execute(
            select(Collection).where(Collection.title == title)
        )
        return self._get_domain_model_or_none(data=result, model=CollectionModel)

    async def get_list(self) -> list[CollectionModel]:
        result: Result = await self.session.execute(
            select(Collection)
        )
        if data := result.scalars().all():
            return [CollectionModel.model_validate(obj=obj, from_attributes=True) for obj in data]
        return []

    async def update(self, id_: UUID, data: dict) -> Optional[CollectionModel]:
        pass

    async def delete(self, id_: UUID) -> bool:
        pass
