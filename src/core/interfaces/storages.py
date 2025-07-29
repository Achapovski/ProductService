from abc import ABC, abstractmethod
from typing import BinaryIO


class AbstractStorageClient(ABC):
    @abstractmethod
    async def upload_object(self, key: str, obj: BinaryIO):
        raise NotImplementedError

    @abstractmethod
    async def download_object(self, key: str):
        raise NotImplementedError

    @abstractmethod
    async def delete_object(self, key: str):
        raise NotImplementedError

    @abstractmethod
    async def get_objects_names(self, key: str):
        raise NotImplementedError

    @abstractmethod
    async def object_post_url(self, key: str):
        raise NotImplementedError

    @abstractmethod
    async def object_get_url(self, key: str):
        raise NotImplementedError
