from app.schemas.users import UserUpdateSchema
from app.settings import get_settings, Settings
from fastapi import Depends, HTTPException, status, BackgroundTasks
from app.repositories.users import UserRepository
from app.schemas.users import UserCreateSchema, UserLoginSchema, UserOutSchema
from app.utils.authentication import create_access_token, decode_token

from app.utils.users import hash_password, verify_password


class UserController:
    def __init__(
        self,
        user_repo: UserRepository = Depends(),
        settings: Settings = Depends(get_settings),
    ):
        self.user_repo = user_repo
        self.settings = settings

    async def get_current_user(self, token: str):
        payload = decode_token(token, self.settings.SECRET_KEY, "HS256")
        email = payload.get("email")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = await self.user_repo.get_user_by_email(email)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user

    async def get_user(self, current_user, user_id: int) -> UserOutSchema:
        if current_user.role != "admin" and current_user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed"
            )
        user = await self.user_repo.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    async def update_user(
        self, current_user, user_id: int, data: UserUpdateSchema
    ) -> UserOutSchema:
        user = await self.get_user(current_user, user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        if current_user.role != "admin" and current_user.id != user_id:
            raise HTTPException(status_code=403, detail="Not allowed")

        if current_user.role != "admin":
            data.role = None
            data.email = None

        if data.email is not None:
            user.email = data.email
        if data.first_name is not None:
            user.first_name = data.first_name
        if data.last_name is not None:
            user.last_name = data.last_name
        if data.role is not None:
            user.role = data.role

        await self.user_repo.update_user(user)
        return user

    async def delete_user(self, current_user, user_id: int):
        user = await self.get_user(current_user, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if current_user.role != "admin" and current_user.id != user_id:
            raise HTTPException(status_code=403, detail="Not allowed")

        await self.user_repo.delete_user(user)
        return {"message": "User deleted"}


class AuthController:
    def __init__(
        self,
        user_repo: UserRepository = Depends(),
        settings: Settings = Depends(get_settings),
    ):
        self.user_repo = user_repo
        self.settings = settings

    async def register_user(self, data: UserCreateSchema) -> UserOutSchema:
        existing = await self.user_repo.get_user_by_email(data.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        user = await self.user_repo.create_user(
            email=data.email,
            password=hash_password(data.password),
            first_name=data.first_name,
            last_name=data.last_name,
            role=data.role or "customer",
        )

        token_data = {"email": user.email, "scope": "verify"}
        verify_token = create_access_token(
            data=token_data,
            secret_key=self.settings.SECRET_KEY,
            algorithm="HS256",
            expires_minutes=self.settings.ACCESS_TOKEN_EXPIRE_MINUTES,  # e.g., 60
        )
        return UserOutSchema(
            id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            role=user.role,
        )

    async def login_user(self, data: UserLoginSchema) -> dict:
        user = await self.user_repo.get_user_by_email(data.email)
        if not user or not verify_password(user.password, data.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
            )

        access_token = create_access_token(
            data={"email": user.email, "role": user.role},
            secret_key=self.settings.SECRET_KEY,
            algorithm="HS256",
            expires_minutes=self.settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        )
        return {"access_token": access_token, "token_type": "bearer"}
