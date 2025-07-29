from src.products.adapters.repositories.products import SQLAlchemyProductsRepository
from src.products.adapters.repositories.colors import SQLAlchemyColorsRepository
from src.products.adapters.repositories.categories import SQLAlchemyCategoriesRepository
from src.products.adapters.repositories.types import SQLAlchemyTypesRepository
from src.products.adapters.repositories.images import SQLAlchemyImagesRepository
from src.products.adapters.repositories.materials import SQLAlchemyMaterialsRepository
from src.products.adapters.repositories.collections import SQLAlchemyCollectionsRepository

__all__ = [
    "SQLAlchemyTypesRepository",
    "SQLAlchemyColorsRepository",
    "SQLAlchemyImagesRepository",
    "SQLAlchemyProductsRepository",
    "SQLAlchemyMaterialsRepository",
    "SQLAlchemyCategoriesRepository",
    "SQLAlchemyCollectionsRepository",
]
