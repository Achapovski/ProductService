from src.core.database.interfaces.units_of_work import SQLAlchemyAbstractUnitOfWork
from src.products.adapters.repositories.secondaries import SQLAlchemyProductsColorsAssociateRepository
from src.products.interfaces.units_of_work import ProductUnitOfWork
from src.products.adapters.repositories import (
    SQLAlchemyProductsRepository,
    SQLAlchemyColorsRepository,
    SQLAlchemyImagesRepository,
    SQLAlchemyTypesRepository,
    SQLAlchemyCategoriesRepository,
    SQLAlchemyMaterialsRepository,
    SQLAlchemyCollectionsRepository,
)


class SQLAlchemyProductsUnitOfWork(SQLAlchemyAbstractUnitOfWork, ProductUnitOfWork):
    async def __aenter__(self):
        uow = await super().__aenter__()
        self.types: SQLAlchemyTypesRepository = SQLAlchemyTypesRepository(session=self.session)
        self.colors: SQLAlchemyColorsRepository = SQLAlchemyColorsRepository(session=self.session)
        self.images: SQLAlchemyImagesRepository = SQLAlchemyImagesRepository(session=self.session)
        self.products: SQLAlchemyProductsRepository = SQLAlchemyProductsRepository(session=self.session)
        self.materials: SQLAlchemyMaterialsRepository = SQLAlchemyMaterialsRepository(session=self.session)
        self.categories: SQLAlchemyCategoriesRepository = SQLAlchemyCategoriesRepository(session=self.session)
        self.collections: SQLAlchemyCollectionsRepository = SQLAlchemyCollectionsRepository(session=self.session)
        self.product_colors: SQLAlchemyProductsColorsAssociateRepository = SQLAlchemyProductsColorsAssociateRepository(
            session=self.session
        )
        return uow
