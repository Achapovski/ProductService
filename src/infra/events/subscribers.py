from typing import Annotated

from asyncpg import UniqueViolationError
from fast_depends import Depends
from faststream.kafka.router import KafkaRouter

from src.app.events.subscribe import YandexCloudEvent
from src.app.use_cases.product_use_case import ProductUseCase
from src.core.settings.settings import settings
from src.infra.entrypoints.dependencies import get_product_use_case
from src.products.domain.models import ImageCreateModel
from src.products.exceptions.exceptions import ProductImageLoadingFailedException, \
    ProductImageNameAlreadyExistsException

kafka_router = KafkaRouter()


@kafka_router.subscriber(settings.KAFKA.TOPICS.PRODUCTS.IMAGES.CREATE)
async def kafka_subscriber(
        data: YandexCloudEvent,
        product_use_case: Annotated[ProductUseCase, Depends(get_product_use_case)]
):
    try:
        product_titles = [title.details.object_id.split("/") for title in data.messages]
        for title in product_titles:
            image = ImageCreateModel(title=title[-1], product_image_title_prefix=title[0])
            return await product_use_case.attach_image_for_product(image=image)
    except UniqueViolationError as err:
        raise ProductImageNameAlreadyExistsException()
    except Exception as err:
        raise ProductImageLoadingFailedException()
