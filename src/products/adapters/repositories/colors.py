from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import Result, select
from sqlalchemy.dialects.postgresql import insert

from src.core.database.interfaces.repositories import SQLAlchemyAbstractRepository
from src.products.adapters.models import Color
from src.products.domain.models.color import ColorModel, ColorCreateModel
from src.products.interfaces.repositories import ColorsAbstractRepository


class SQLAlchemyColorsRepository(SQLAlchemyAbstractRepository, ColorsAbstractRepository):
    async def add(self, model: ColorCreateModel) -> ColorModel:
        pass

    async def add_many(self, model_list: list[ColorCreateModel]) -> list[ColorModel]:
        result: Result = await self.session.execute(
            insert(Color).values(
                [{"id": uuid4(), **color.model_dump()} for color in model_list]
            )
            .on_conflict_do_update(
                index_elements={"title"},
                set_={"title": insert(Color).excluded.title}
            )
            .returning(Color)
        )
        if data := result.scalars().all():
            return [ColorModel.model_validate(obj=obj, from_attributes=True) for obj in data]
        return []

    async def get(self, id_: UUID) -> Optional[ColorModel]:
        result: Result = await self.session.execute(
            select(Color).where(Color.id == str(id_))
        )
        return self._get_domain_model_or_none(data=result, model=ColorModel)

    async def get_by_title(self, title: str) -> Optional[ColorModel]:
        result: Result = await self.session.execute(
            select(Color).where(Color.title == title)
        )
        return self._get_domain_model_or_none(data=result, model=ColorModel)

    async def get_list(self) -> list[ColorModel]:
        result: Result = await self.session.execute(
            select(Color)
        )
        if data := result.scalars().all():
            return [ColorModel.model_validate(obj=obj, from_attributes=True) for obj in data]
        return []

    async def update(self, id_: UUID, data: dict) -> Optional[ColorModel]:
        pass

    async def delete(self, id_: UUID) -> bool:
        pass
