from abc import ABC
from typing import Type, Optional

from sqlalchemy import Result
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.interfaces.repositories import AbstractRepository
from src.core.interfaces.models import AbstractModel


class SQLAlchemyAbstractRepository(AbstractRepository, ABC):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    @staticmethod
    def _get_domain_model_or_none[T:Type[AbstractModel]](data: Result, model: T) -> Optional[Type[T]]:
        if result := data.scalar_one_or_none():
            return model.model_validate(result, from_attributes=True)
        return None
