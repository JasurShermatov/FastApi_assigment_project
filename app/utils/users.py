from passlib.hash import bcrypt
from enum import Enum


class UserRole(Enum):
    ADMIN = "admin"
    CUSTOMER = "customer"


def hash_password(plain_password: str) -> str:
    return bcrypt.hash(plain_password)


def verify_password(hashed_password: str, plain_password: str) -> bool:
    return bcrypt.verify(plain_password, hashed_password)
