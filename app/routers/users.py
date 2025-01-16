from fastapi import APIRouter, Depends, Path, status
from fastapi.security import OAuth2PasswordBearer

from app.controllers.users import UserController
from app.schemas.users import UserOutSchema, UserUpdateSchema

router = APIRouter(prefix="/users", tags=["Users"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@router.get("/me", response_model=UserOutSchema)
async def get_myself(
    token: str = Depends(oauth2_scheme), controller: UserController = Depends()
):
    current_user = await controller.get_current_user(token)
    return current_user


@router.get("/{user_id}", response_model=UserOutSchema)
async def get_user(
    user_id: int = Path(...),
    token: str = Depends(oauth2_scheme),
    controller: UserController = Depends(),
):
    current_user = await controller.get_current_user(token)
    user = await controller.get_user(current_user, user_id)
    return user


@router.put("/{user_id}/", response_model=UserOutSchema)
@router.patch("/{user_id}/", response_model=UserOutSchema)
async def update_user(
    user_id: int,
    data: UserUpdateSchema,
    token: str = Depends(oauth2_scheme),
    controller: UserController = Depends(),
):
    current_user = await controller.get_current_user(token)
    updated = await controller.update_user(current_user, user_id, data)
    return updated


@router.delete("/{user_id}/")
async def delete_user(
    user_id: int,
    token: str = Depends(oauth2_scheme),
    controller: UserController = Depends(),
):
    current_user = await controller.get_current_user(token)
    return await controller.delete_user(current_user, user_id)
