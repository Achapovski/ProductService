from abc import ABC, abstractmethod
from typing import Self


class AbstractModel(ABC):
    # Base abstract model, from which any domain model should be inherited.
    @abstractmethod
    def model_dump(self, *args, **kwargs) -> dict:
        raise NotImplementedError

    @abstractmethod
    def model_validate(self, *args, **kwargs) -> Self:
        raise NotImplementedError

    def model_dump_to_grps_obj(self) -> dict:
        return {str(key): str(value) for key, value in self.model_dump().items()}


class AssociateModel(ABC):
    @abstractmethod
    def model_dump(self, *args, **kwargs) -> dict:
        raise NotImplementedError

    @abstractmethod
    def model_associate_list(self) -> list[dict]:
        raise NotImplementedError
