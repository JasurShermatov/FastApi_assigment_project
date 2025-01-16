from typing import Sequence

from fastapi import Depends, HTTPException, status
from app.repositories.orders import OrderRepository
from app.repositories.products import ProductRepository
from app.models.orders import Order
from app.models.orders import OrderDetail
from app.schemas.orders import OrderCreateSchema


class OrderController:
    def __init__(
        self,
        order_repo: OrderRepository = Depends(),
        product_repo: ProductRepository = Depends(),
    ):
        self.order_repo = order_repo
        self.product_repo = product_repo

    async def list_orders(self) -> list[Order]:
        return await self.order_repo.list_orders()

    async def get_order_details(self, order_id: int):
        order = await self.order_repo.get_order_by_id(order_id)
        if not order:
            raise HTTPException(404, "Order not found")
        _ = order.order_details
        order_dict: dict[str, list | object] = {
            "id": order.id,
            "user_id": order.user_id,
            "status": order.status,
            "total_amount": order.total_amount,
            "created_at": order.created_at,
            "order_details": [],
        }
        for d in order.order_details:
            order_dict["order_details"].append(
                {
                    "product_id": d.product_id,
                    "quantity": d.quantity,
                    "unit_price": d.unit_price,
                }
            )

        return order_dict

    async def create_order(self, user_id: int, data: OrderCreateSchema) -> Order:
        total = 0.0
        details = []

        for item in data.items:
            product = await self.product_repo.get_product_by_id(item.product_id)
            if not product:
                raise HTTPException(status_code=404, detail="Product not found")

            line_total = product.price * item.quantity
            total += line_total

            detail = OrderDetail(
                product_id=item.product_id,
                quantity=item.quantity,
                unit_price=product.price,
            )
            details.append(detail)

        order = Order(
            user_id=user_id,
            status="pending",
            total_amount=total,
        )
        created_order = await self.order_repo.create_order(order, details)
        fresh_order = await self.order_repo.get_order_by_id(created_order.id)

        return fresh_order

    async def get_order_by_id(self, order_id: int) -> Order:
        order = await self.order_repo.get_order_by_id(order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order

    async def list_orders_by_user(self, user_id: int) -> Sequence[Order]:
        return await self.order_repo.list_orders_by_user(user_id)

    async def get_order_status(self, order_id: int) -> str:
        order = await self.get_order_by_id(order_id)
        return order.status
