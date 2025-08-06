from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status, HTTPException, Body

from src.app.entrypoints.dependencies import get_product_service, get_product_use_case
from src.app.use_cases.product_use_case import ProductUseCase
from src.products.domain.models import ProductPreCreateModel, ProductSafeModel, ProductExistsParamsModel
from src.products.domain.models.product import ProductSafeUpdateModel, ProductModel
from src.products.services.service import ProductService

router = APIRouter()


@router.post(
    path="/",
    # response_model=ProductSafeModel
)
async def create_product(
        product: ProductPreCreateModel,
        images: Annotated[list[str], Body(embed=True)],
        product_use_case: Annotated[ProductUseCase, Depends(get_product_use_case)]
):
    if product := await product_use_case.create_product(product=product, images=images):
        return product
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.get(
    path="/new",
    response_model=ProductExistsParamsModel,
    status_code=status.HTTP_200_OK
)
async def init_create_product(
        product_use_case: Annotated[ProductUseCase, Depends(get_product_use_case)]
) -> ProductExistsParamsModel:
    return await product_use_case.get_product_attrs()


@router.post(
    path="/images/presign",
    status_code=status.HTTP_200_OK
)
async def get_presign_urls(
        filenames: Annotated[list[str], Body(embed=True)],
        product_use_case: Annotated[ProductUseCase, Depends(get_product_use_case)]
):
    return await product_use_case.generate_presign_post_urls(filenames=filenames)


@router.get(
    path="/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=ProductSafeModel
)
async def get_product(
        product_id: UUID,
        product_use_case: Annotated[ProductUseCase, Depends(get_product_use_case)]
) -> ProductSafeModel:
    return await product_use_case.get_product(product_id=product_id)


@router.get(
    path="/",
    response_model=list[ProductSafeModel],
    status_code=status.HTTP_200_OK
)
async def get_products(
        product_use_case: Annotated[ProductUseCase, Depends(get_product_use_case)]
) -> list[ProductSafeModel | ProductModel]:
    products = await product_use_case.get_products()
    return products


@router.patch(
    path="/{product_id}",
    response_model=ProductSafeUpdateModel,
    status_code=status.HTTP_200_OK
)
async def update_product(
        product_id: UUID,
        product: ProductSafeUpdateModel,
        product_service: Annotated[ProductService, Depends(get_product_service)]
) -> ProductSafeUpdateModel:
    product = await product_service.update_product(id_=product_id, product=product)
    return ProductSafeUpdateModel(**product.model_dump())


@router.delete(
    path="/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_product(
        product_id: UUID,
        product_use_case: Annotated[ProductUseCase, Depends(get_product_use_case)]
):
    return await product_use_case.delete_product(product_id=product_id)
