from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import Result, select
from sqlalchemy.dialects.postgresql import insert

from src.core.database.interfaces.repositories import SQLAlchemyAbstractRepository
from src.products.adapters.models import Category
from src.products.domain.models.category import CategoryCreateModel, CategoryModel
from src.products.interfaces.repositories import CategoryAbstractRepository


class SQLAlchemyCategoriesRepository(SQLAlchemyAbstractRepository, CategoryAbstractRepository):
    async def add(self, model: CategoryCreateModel) -> CategoryModel:
        result: Result = await self.session.execute(
            insert(Category).values(id=uuid4(), **model.model_dump()).returning(Category)
        )
        return self._get_domain_model_or_none(data=result, model=CategoryModel)

    async def add_many(self, model_list: list[CategoryCreateModel]) -> list[CategoryModel]:
        result: Result = await self.session.execute(
            insert(Category).values(
                [{"id": uuid4(), **color.model_dump()} for color in model_list]
            )
            .on_conflict_do_update(
                index_elements={"title"},
                set_={"title": insert(Category).excluded.title}
            )
            .returning(Category)
        )
        if data := result.scalars().all():
            return [CategoryModel.model_validate(obj=obj, from_attributes=True) for obj in data]
        return []

    async def get(self, id_: UUID) -> Optional[CategoryModel]:
        result: Result = await self.session.execute(
            select(Category).where(Category.id == str(id_))
        )
        return self._get_domain_model_or_none(data=result, model=CategoryModel)

    async def get_by_title(self, title: str) -> Optional[CategoryModel]:
        result: Result = await self.session.execute(
            select(Category).where(Category.title == title)
        )
        return self._get_domain_model_or_none(data=result, model=CategoryModel)

    async def get_list(self) -> list[CategoryModel]:
        result: Result = await self.session.execute(
            select(Category)
        )
        if data := result.scalars().all():
            return [CategoryModel.model_validate(obj=obj, from_attributes=True) for obj in data]
        return []

    async def update(self, id_: UUID, data: dict) -> Optional[CategoryModel]:
        pass

    async def delete(self, id_: UUID) -> bool:
        pass
