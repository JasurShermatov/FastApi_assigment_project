from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Sequence
from app.controllers.orders import OrderController
from app.schemas.orders import OrderCreateSchema, OrderOutSchema
from app.utils.authentication import get_current_user


router = APIRouter(prefix="/api/orders", tags=["Orders"])


@router.get("", response_model=List[OrderOutSchema])
async def list_orders(
    current_user=Depends(get_current_user),
    controller: OrderController = Depends(),
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    return await controller.list_orders()


@router.get("/{order_id}")
async def get_order(
    order_id: int,
    controller: OrderController = Depends(),
):
    return await controller.get_order_details(order_id)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_order(
    data: OrderCreateSchema,
    current_user=Depends(get_current_user),
    controller: OrderController = Depends(),
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    return await controller.create_order(user_id=current_user.id, data=data)


@router.get("/customer/{customer_id}", response_model=Sequence[OrderOutSchema])
async def get_customer_orders(
    customer_id: int,
    current_user=Depends(get_current_user),
    controller: OrderController = Depends(),
):
    if current_user.role == "customer" and current_user.id != customer_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return await controller.list_orders_by_user(customer_id)


@router.get("/{order_id}/status")
async def get_order_status(
    order_id: int,
    current_user=Depends(get_current_user),
    controller: OrderController = Depends(),
):
    order = await controller.get_order_by_id(order_id)
    if current_user.role == "customer" and order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return {"order_id": order.id, "status": order.status}
