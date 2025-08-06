from fastapi import status

from src.app.exceptions.exceptions import ApplicationBaseException


class ProductException(ApplicationBaseException):
    pass


class ProductNotFoundException(ProductException):
    DETAIL = "Product not found!"
    STATUS_CODE = status.HTTP_404_NOT_FOUND


class ProductAlreadyExistsException(ProductException):
    DETAIL = "Product already exists!"
    STATUS_CODE = status.HTTP_409_CONFLICT
