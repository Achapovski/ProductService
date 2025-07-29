from typing import BinaryIO

from types_aiobotocore_s3.client import S3Client
from types_aiobotocore_s3.type_defs import ObjectTypeDef

from src.infra.interfaces.storages import AbstractS3StorageClient


class S3StorageClient(AbstractS3StorageClient):
    async def upload_object(self, key: str, obj: BinaryIO):
        async with self.get_client() as client:
            client: S3Client
        return await client.put_object(Bucket=self.settings.BUCKET, Key=key, Body=obj)

    async def get_objects_names(self, key: str) -> list[ObjectTypeDef]:
        async with self.get_client() as client:
            client: S3Client
            res = await client.list_objects(Bucket=self.settings.BUCKET, Prefix=key)
        return [obj for obj in res.get("Contents", [])]

    async def download_object(self, key: str):
        pass

    async def delete_object(self, key: str):
        pass

    async def object_post_url(self, key: str):
        async with self.get_client() as client:
            client: S3Client
        return await client.generate_presigned_post(Bucket=self.settings.BUCKET, Key=key)

    async def object_get_url(self, key: str) -> str:
        async with self.get_client() as client:
            client: S3Client
        return await client.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": self.settings.BUCKET, "Key": key},
            ExpiresIn=3600
        )
