from uuid import UUID
from abc import ABC, abstractmethod
from typing import Optional

from src.core.interfaces.repositories import AbstractRepository
from src.products.domain.models.category import CategoryModel, CategoryCreateModel
from src.products.domain.models.collection import CollectionCreateModel, CollectionModel
from src.products.domain.models.image import ImageModel, ImageCreateModel
from src.products.domain.models.material import MaterialModel, MaterialCreateModel
from src.products.domain.models.product import ProductModel
from src.products.domain.models.color import ColorModel, ColorCreateModel
from src.products.domain.models.type import TypeCreateModel, TypeModel


class ProductsAbstractRepository(AbstractRepository, ABC):
    @abstractmethod
    async def add(self, model: ProductModel) -> ProductModel:
        raise NotImplementedError

    @abstractmethod
    async def get_by_title(self, title: str) -> Optional[ProductModel]:
        raise NotImplementedError

    @abstractmethod
    async def get_list(self):
        raise NotImplementedError

    @abstractmethod
    async def get(self, id_: UUID) -> Optional[ProductModel]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, id_: UUID, data: dict) -> Optional[ProductModel]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id_: UUID) -> bool:
        raise NotImplementedError


class ColorsAbstractRepository(AbstractRepository, ABC):
    @abstractmethod
    async def add(self, model: ColorCreateModel) -> ColorModel:
        raise NotImplementedError

    @abstractmethod
    async def add_many(self, model_list: list[ColorCreateModel]) -> list[ColorModel]:
        raise NotImplementedError

    @abstractmethod
    async def get(self, id_: UUID) -> Optional[ColorModel]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_title(self, title: str) -> Optional[ColorModel]:
        raise NotImplementedError

    @abstractmethod
    async def get_list(self) -> list[ColorModel]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, id_: UUID, data: dict) -> Optional[ColorModel]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id_: UUID) -> bool:
        raise NotImplementedError


class ImagesAbstractRepository(AbstractRepository, ABC):
    @abstractmethod
    async def add(self, model: ImageCreateModel) -> ImageModel:
        raise NotImplementedError

    @abstractmethod
    async def get(self, id_: UUID) -> Optional[ImageModel]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, id_: UUID, data: dict) -> Optional[ImageModel]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id_: UUID) -> bool:
        raise NotImplementedError


class CategoryAbstractRepository(AbstractRepository, ABC):
    @abstractmethod
    async def add(self, model: CategoryCreateModel) -> CategoryModel:
        raise NotImplementedError

    @abstractmethod
    async def add_many(self, model_list: list[CategoryCreateModel]) -> list[CategoryModel]:
        raise NotImplementedError

    @abstractmethod
    async def get(self, id_: UUID) -> Optional[CategoryModel]:
        raise NotImplementedError

    @abstractmethod
    async def get_list(self) -> list[CategoryModel]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_title(self, title: str) -> Optional[CategoryModel]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, id_: UUID, data: dict) -> Optional[CategoryModel]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id_: UUID) -> bool:
        raise NotImplementedError


class CollectionsAbstractRepository(AbstractRepository, ABC):
    @abstractmethod
    async def add(self, model: CollectionCreateModel) -> CollectionModel:
        raise NotImplementedError

    @abstractmethod
    async def get(self, id_: UUID) -> Optional[CollectionModel]:
        raise NotImplementedError

    @abstractmethod
    async def get_list(self) -> list[CollectionModel]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_title(self, title: str) -> Optional[CollectionModel]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, id_: UUID, data: dict) -> Optional[CollectionModel]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id_: UUID) -> bool:
        raise NotImplementedError


class MaterialsAbstractRepository(AbstractRepository, ABC):
    @abstractmethod
    async def add(self, model: MaterialCreateModel) -> MaterialModel:
        raise NotImplementedError

    @abstractmethod
    async def add_many(self, model_list: list[MaterialCreateModel]) -> list[MaterialModel]:
        raise NotImplementedError

    @abstractmethod
    async def get(self, id_: UUID) -> Optional[MaterialModel]:
        raise NotImplementedError

    @abstractmethod
    async def get_list(self) -> list[MaterialModel]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_title(self, title: str) -> Optional[MaterialModel]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, id_: UUID, data: dict) -> Optional[MaterialModel]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id_: UUID) -> bool:
        raise NotImplementedError


class TypesAbstractRepository(AbstractRepository, ABC):
    @abstractmethod
    async def add(self, model: TypeCreateModel) -> TypeModel:
        raise NotImplementedError

    @abstractmethod
    async def get(self, id_: UUID) -> Optional[TypeModel]:
        raise NotImplementedError

    @abstractmethod
    async def get_list(self) -> list[TypeModel]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_title(self, title: str) -> Optional[TypeModel]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, id_: UUID, data: dict) -> Optional[TypeModel]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id_: UUID) -> bool:
        raise NotImplementedError
