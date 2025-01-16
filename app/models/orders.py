from datetime import datetime
from sqlalchemy import ForeignKey, Float, String, text, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base


class Order(Base):
    __tablename__ = "orders"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    status: Mapped[str] = mapped_column(String(15), nullable=False)
    total_amount: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    created_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )

    order_details: Mapped[list["OrderDetail"]] = relationship(  # noqa
        "OrderDetail",
        back_populates="order",
        cascade="all, delete-orphan",
    )


class OrderDetail(Base):
    __tablename__ = "order_details"

    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price: Mapped[float] = mapped_column(Float, nullable=False)

    order = relationship("Order", back_populates="order_details")
