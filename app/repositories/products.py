from typing import Optional, Sequence
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.products import Product
from app.database import get_general_session


class ProductRepository:
    def __init__(self, session: AsyncSession = Depends(get_general_session)):
        self.session = session

    async def create_product(self, **kwargs) -> Product:
        product = Product(**kwargs)
        self.session.add(product)
        await self.session.commit()
        await self.session.refresh(product)
        return product

    async def get_product_by_id(self, product_id: int) -> Optional[Product]:
        result = await self.session.execute(
            select(Product).where(Product.id == product_id)
        )
        return result.scalars().first()

    async def update_product(self, product: Product) -> Product:
        self.session.add(product)
        await self.session.commit()
        await self.session.refresh(product)
        return product

    async def delete_product(self, product: Product):
        await self.session.delete(product)
        await self.session.commit()

    async def list_products(self):
        result = await self.session.execute(select(Product))
        return result.scalars().all()
