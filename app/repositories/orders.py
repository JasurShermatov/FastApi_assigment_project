from fastapi import Depends
from typing import List, Optional, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.models.orders import Order
from app.models.orders import OrderDetail
from app.database import get_general_session


class OrderRepository:
    def __init__(self, session: AsyncSession = Depends(get_general_session)):
        self.session = session

    async def list_orders(self) -> Sequence[Order]:
        stmt = select(Order).options(selectinload(Order.order_details))
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create_order(self, order: Order, details: List[OrderDetail]) -> Order:
        self.session.add(order)
        await self.session.flush()

        for detail in details:
            detail.order_id = order.id
            self.session.add(detail)

        await self.session.commit()
        await self.session.refresh(order)
        return order

    async def get_order_by_id(self, order_id: int) -> Optional[Order]:
        stmt = (
            select(Order)
            .where(Order.id == order_id)
            .options(selectinload(Order.order_details))
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def list_orders_by_user(self, user_id: int) -> Sequence[Order]:
        stmt = (
            select(Order)
            .where(Order.user_id == user_id)
            .options(selectinload(Order.order_details))
        )
        result = await self.session.execute(stmt)
        orders = result.scalars().all()
        return orders

    async def update_order(self, order: Order) -> Order:
        self.session.add(order)
        await self.session.commit()
        await self.session.refresh(order)
        return order
