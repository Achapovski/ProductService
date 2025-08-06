from typing import Annotated

from fast_depends import Depends
from faststream.kafka.router import KafkaRouter

from src.app.events.subscribe import YandexCloudEvent
from src.app.use_cases.product_use_case import ProductUseCase
from src.infra.entrypoints.dependencies import get_product_use_case
from src.products.domain.models import ImageCreateModel

kafka_router = KafkaRouter()


@kafka_router.subscriber("test_topic")
async def kafka_subscriber(
        data: YandexCloudEvent,
        product_use_case: Annotated[ProductUseCase, Depends(get_product_use_case)]
):
    print(product_title := data.messages[0].details.object_id.split("/"))
    image = ImageCreateModel(title=product_title[-1], product_image_title_prefix=product_title[0])
    print(await product_use_case.attach_image_for_product(image=image))
