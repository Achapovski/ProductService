from src.products.domain.models.product import *
from src.products.domain.models.category import *
from src.products.domain.models.color import *
from src.products.domain.models.type import *
from src.products.domain.models.image import *
from src.products.domain.models.collection import *
from src.products.domain.models.material import *

ProductModel.model_rebuild()
ProductSafeModel.model_rebuild()
ProductUpdateModel.model_rebuild()
ProductSafeUpdateModel.model_rebuild()
