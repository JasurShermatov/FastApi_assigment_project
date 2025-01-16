from fastapi import Depends, HTTPException, status
from app.repositories.products import ProductRepository
from app.schemas.products import (
    ProductCreateSchema,
    ProductUpdateSchema,
)
from app.models.products import Product


class ProductController:
    def __init__(self, product_repo: ProductRepository = Depends()):
        self.product_repo = product_repo

    async def create_product(self, data: ProductCreateSchema) -> Product:
        product = await self.product_repo.create_product(
            **data.model_dump(exclude_unset=True)
        )
        return product

    async def get_product(self, product_id: int) -> Product:
        product = await self.product_repo.get_product_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product

    async def update_product(
        self, product_id: int, data: ProductUpdateSchema
    ) -> Product:
        product = await self.get_product(product_id)
        update_data = data.dict(exclude_unset=True)
        for k, v in update_data.items():
            setattr(product, k, v)
        return await self.product_repo.update_product(product)

    async def delete_product(self, product_id: int):
        product = await self.get_product(product_id)
        await self.product_repo.delete_product(product)

    async def list_products(self):
        return await self.product_repo.list_products()
