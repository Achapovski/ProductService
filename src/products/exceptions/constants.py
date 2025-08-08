from dataclasses import dataclass


@dataclass
class ErrorDetails:
    PRODUCT_NOT_FOUND: str = "Product not found."
    PRODUCT_ALREADY_EXISTS: str = "Product already exists!"
    PRODUCT_NOTHING_FOR_UPDATE: str = "Nothing for update!"
    PRODUCT_IMAGE_LOADING_FAILED: str = "Image loading failed."
    PRODUCT_IMAGE_ALREADY_EXIST: str = "Image with this name already exist."

