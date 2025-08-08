from typing import Any

from pydantic import BaseModel


class ExceptionInfoModel(BaseModel):
    message: Any
    detail: str | None = None
