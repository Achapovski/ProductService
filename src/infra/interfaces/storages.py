from abc import ABC
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from aiobotocore.session import get_session
from types_aiobotocore_s3 import S3Client

from src.core.interfaces.storages import AbstractStorageClient
from src.core.settings.schemes import S3Settings


class AbstractS3StorageClient(AbstractStorageClient, ABC):
    def __init__(self, settings: S3Settings):
        self.settings: S3Settings = settings
        self.session = get_session()
        self.config = {
            "aws_access_key_id": self.settings.ACCESS_KEY_ID,
            "aws_secret_access_key": self.settings.SECRET_ACCESS_KEY,
            "endpoint_url": self.settings.ENDPOINT_URL,
            "service_name": self.settings.SERVICE_NAME
        }
        self.client = None

    @asynccontextmanager
    async def get_client(self) -> AsyncGenerator[S3Client, None]:
        if self.client:
            yield self.client
        else:
            async with self.session.create_client(**self.config) as client:
                self.client = client
                yield self.client
