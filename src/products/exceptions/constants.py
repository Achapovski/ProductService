from dataclasses import dataclass


@dataclass
class ErrorDetails:
    PRODUCT_NOT_FOUND: str = "Product not found."
    PRODUCT_ALREADY_EXISTS: str = "Product already exists"

