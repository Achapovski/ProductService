from abc import ABC

from src.core.interfaces.units_of_work import AbstractUnitOfWork
from src.products.adapters.repositories import (
    SQLAlchemyCategoriesRepository,
    SQLAlchemyCollectionsRepository,
    SQLAlchemyImagesRepository,
    SQLAlchemyMaterialsRepository,
    SQLAlchemyProductsRepository,
    SQLAlchemyColorsRepository,
    SQLAlchemyTypesRepository,
)
from src.products.adapters.repositories.secondaries import SQLAlchemyProductsColorsAssociateRepository


class ProductUnitOfWork(AbstractUnitOfWork, ABC):
    types: SQLAlchemyTypesRepository
    colors: SQLAlchemyColorsRepository
    images: SQLAlchemyImagesRepository
    products: SQLAlchemyProductsRepository
    materials: SQLAlchemyMaterialsRepository
    categories: SQLAlchemyCategoriesRepository
    collections: SQLAlchemyCollectionsRepository
    product_colors: SQLAlchemyProductsColorsAssociateRepository
