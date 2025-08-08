from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from src.app.exceptions.constants import ErrorDetails
from src.app.exceptions.models import ExceptionInfoModel
from src.products.exceptions.exceptions import ProductBaseException


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(ProductBaseException)
    def handle_product_exception(request: Request, exc: ProductBaseException):
        return JSONResponse(
            status_code=exc.STATUS_CODE,
            content=ExceptionInfoModel(message=exc.MESSAGE, detail=exc.DETAIL).model_dump()
        )

    @app.exception_handler(ValidationError)
    def handle_validation_error(request: Request, exc: ValidationError):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=ExceptionInfoModel(message=exc.json()).model_dump()
        )

    @app.exception_handler(Exception)
    def handle_common_exception(request: Request, exc: Exception):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ExceptionInfoModel(message=ErrorDetails.SERVER_ERROR).model_dump()
        )
