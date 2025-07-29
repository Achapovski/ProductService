from fastapi import FastAPI, Request, HTTPException, status
from pydantic import ValidationError

from src.domains.products.exceptions.exceptions import ProductException


def exception(app: FastAPI):
    @app.exception_handler(ProductException)
    def handle_product_exception(request: Request, exc: ProductException):
        raise HTTPException(
            status_code=exc.STATUS_CODE,
            detail=exc.DETAIL
        )

    @app.exception_handler(ValidationError)
    def handle_validation_error(request: Request, exc: ValidationError):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=exc.json()
        )
