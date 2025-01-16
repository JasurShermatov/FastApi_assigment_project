from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.controllers.products import ProductController
from app.schemas.products import (
    ProductCreateSchema,
    ProductOutSchema,
    ProductUpdateSchema,
)
from app.utils.authentication import get_current_user

router = APIRouter(prefix="/api/products", tags=["Products"])


@router.get("", response_model=List[ProductOutSchema])
async def list_products(
    controller: ProductController = Depends(),
):
    return await controller.list_products()


@router.post("/", response_model=ProductOutSchema, status_code=status.HTTP_201_CREATED)
async def create_product(
    data: ProductCreateSchema,
    current_user=Depends(get_current_user),
    controller: ProductController = Depends(),
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    return await controller.create_product(data)


@router.get("/{product_id}", response_model=ProductOutSchema)
async def get_product(
    product_id: int,
    controller: ProductController = Depends(),
):
    return await controller.get_product(product_id)


@router.put("/{product_id}/", response_model=ProductOutSchema)
async def update_product(
    product_id: int,
    data: ProductUpdateSchema,
    current_user=Depends(get_current_user),
    controller: ProductController = Depends(),
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    return await controller.update_product(product_id, data)


@router.delete("/{product_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int,
    current_user=Depends(get_current_user),
    controller: ProductController = Depends(),
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    await controller.delete_product(product_id)
    return None
