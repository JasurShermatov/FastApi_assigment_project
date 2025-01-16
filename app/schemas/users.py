from pydantic import BaseModel, ConfigDict
from typing import Optional


class UserCreateSchema(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str
    role: Optional[str] = "customer"


class UserLoginSchema(BaseModel):
    email: str
    password: str


class UserOutSchema(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    role: str

    model_config = ConfigDict(from_attributes=True)


class UserUpdateSchema(BaseModel):
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[str] = None  # Only admin can set role


class TokenSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"
