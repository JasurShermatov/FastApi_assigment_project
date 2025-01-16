from datetime import datetime
from sqlalchemy import String, text, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from pydantic import EmailStr

from app.models.base import Base
from app.utils.users import UserRole


class User(Base):
    __tablename__ = "users"

    password: Mapped[str] = mapped_column(String(255))
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    email: Mapped[EmailStr] = mapped_column(String(254), unique=True, index=True)
    role: Mapped[UserRole] = mapped_column(String(50), default=UserRole.CUSTOMER.value)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("TIMEZONE('utc', now())")
    )
