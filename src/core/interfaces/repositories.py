from uuid import UUID
from abc import ABC, abstractmethod
from typing import Optional

from src.core.interfaces.models import AbstractModel


class AbstractRepository(ABC):
    @abstractmethod
    async def add(self, model: AbstractModel) -> AbstractModel:
        raise NotImplementedError

    @abstractmethod
    async def get(self, id_: UUID) -> Optional[AbstractModel]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, id_: UUID, data: dict) -> Optional[AbstractModel]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id_: UUID) -> bool:
        raise NotImplementedError
