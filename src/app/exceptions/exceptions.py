from fastapi import status

from src.app.exceptions.constants import ErrorDetails
from src.core.interfaces.exceptions import AbstractApplicationBaseException


# TODO: FIX overhead set (Абстрактная модель принимает дочерние объекты исключений)
class ApplicationBaseException(AbstractApplicationBaseException):
    STATUS_CODE: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    DETAIL: str = ErrorDetails.SERVER_ERROR
