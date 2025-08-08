from fastapi import status

from src.app.exceptions.exceptions import ApplicationBaseException
from src.products.exceptions.constants import ErrorDetails


class ProductBaseException(ApplicationBaseException):
    pass


class ProductNotFoundException(ProductBaseException):
    MESSAGE = ErrorDetails.PRODUCT_NOT_FOUND
    STATUS_CODE = status.HTTP_404_NOT_FOUND


class ProductAlreadyExistsException(ProductBaseException):
    MESSAGE = ErrorDetails.PRODUCT_ALREADY_EXISTS
    STATUS_CODE = status.HTTP_409_CONFLICT


class ProductNothingForUpdateException(ProductBaseException):
    MESSAGE = ErrorDetails.PRODUCT_NOTHING_FOR_UPDATE
    STATUS_CODE = status.HTTP_204_NO_CONTENT


class ProductImageLoadingFailedException(ProductBaseException):
    MESSAGE = ErrorDetails.PRODUCT_IMAGE_LOADING_FAILED
    STATUS_CODE = status.HTTP_400_BAD_REQUEST


class ProductImageNameAlreadyExistsException(ProductBaseException):
    MESSAGE = ErrorDetails.PRODUCT_IMAGE_ALREADY_EXIST
    STATUS_CODE = status.HTTP_409_CONFLICT
