from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import Result, select, insert

from src.core.database.interfaces.repositories import SQLAlchemyAbstractRepository
from src.products.adapters.models import Image
from src.products.domain.models.image import ImageCreateModel, ImageModel
from src.products.domain.models.product import ProductModel
from src.products.interfaces.repositories import ImagesAbstractRepository


class SQLAlchemyImagesRepository(SQLAlchemyAbstractRepository, ImagesAbstractRepository):
    async def add(self, model: ImageCreateModel) -> ImageModel:
        result: Result = await self.session.execute(
            insert(Image).values(id=uuid4(), **model.model_dump()).returning(Image)
        )
        return self._get_domain_model_or_none(data=result, model=ImageModel)

    async def get(self, id_: UUID) -> Optional[ImageModel]:
        result: Result = await self.session.execute(
            select(Image).where(Image.id == str(id_))
        )
        return self._get_domain_model_or_none(data=result, model=ImageModel)

    async def update(self, id_: UUID, data: dict) -> Optional[ProductModel]:
        pass

    async def delete(self, id_: UUID) -> bool:
        pass
