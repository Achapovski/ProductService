from typing import Optional

from grpc.aio import server, ServicerContext
from grpc import StatusCode
from google.protobuf.message import Message
from asyncpg.exceptions import UniqueViolationError
from sqlalchemy.exc import IntegrityError

from src.core.grpc.protos import product_service_pb2_grpc, product_service_pb2
from src.core.settings.schemes.grpc import GRPCSettings
from src.products.domain.models.product import ProductSafeUpdateModel, ProductCreateModel
from src.products.exceptions.constants import ErrorDetails as DomainErrorDetails
from src.products.services.service import ProductService


class Service(product_service_pb2_grpc.ProductServiceServicer):
    def __init__(self, product_service: ProductService, settings: GRPCSettings):
        super().__init__()
        self.server: Optional[server] = None
        self.settings: GRPCSettings = settings
        self.product_service: ProductService = product_service

    async def create_product(self, request: Message, context: ServicerContext) -> None:
        product_for_create = ProductCreateModel.model_validate(
            {key.name: value for key, value in request.ListFields()},
            from_attributes=True
        )
        try:
            if product := await self.product_service.create_product(product=product_for_create):
                return product_service_pb2.CreateProductResponse(product={**product.model_dump_to_grps_obj()})
        except (UniqueViolationError, IntegrityError) as err:
            await context.abort(code=StatusCode.ALREADY_EXISTS, details=DomainErrorDetails.PRODUCT_ALREADY_EXISTS)

    async def get_product(self, request: Message, context: ServicerContext) -> None:
        if product := await self.product_service.get_product(id_=request.id):
            return product_service_pb2.ProductByIdResponse(**product.model_dump_to_grps_obj())
        await context.abort(code=StatusCode.NOT_FOUND, details=DomainErrorDetails.PRODUCT_NOT_FOUND)

    async def get_products(self, request: Message, context: ServicerContext) -> None:
        if products := await self.product_service.get_product_list():
            return product_service_pb2.ProductListResponse(
                products=[product.model_dump_to_grps_obj() for product in products]
            )
        await context.abort(code=StatusCode.NOT_FOUND, details=DomainErrorDetails.PRODUCT_NOT_FOUND)

    async def update_product(self, request: Message, context: ServicerContext) -> None:
        product = await self.product_service.update_product(
            id_=request.id,
            product=ProductSafeUpdateModel.model_validate({key.name: value for key, value in request.ListFields()})
        )
        if product:
            return product_service_pb2.UpdateProductResponse(product=product.model_dump_to_grps_obj())
        await context.abort(StatusCode.NOT_FOUND, "Такого товара нет")

    async def delete_product(self, request: Message, context: ServicerContext) -> None:
        product = await self.product_service.delete_product(id_=request.product_id)
        return product_service_pb2.DeleteProductResponse(deleted=product)

    async def run(self) -> None:
        self.server = server()
        product_service_pb2_grpc.add_ProductServiceServicer_to_server(servicer=self, server=self.server)
        self.server.add_insecure_port(self.settings.target_address)
        await self.server.start()

    async def stop(self) -> None:
        await self.server.stop(self.settings.SERVER_STOP_TIMEOUT)
