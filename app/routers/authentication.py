from fastapi import APIRouter, Depends, status
from app.controllers.users import AuthController, UserController
from app.repositories.users import UserRepository
from app.schemas.users import UserLoginSchema, UserCreateSchema

router = APIRouter()


@router.post(
    "/login/",
    status_code=status.HTTP_200_OK,
)
async def login_user(
    user: UserLoginSchema,
    user_repo: AuthController = Depends(),
):
    return await user_repo.login_user(user)


@router.post(
    "/register/",
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    user: UserCreateSchema,
    user_repo: AuthController = Depends(),
):
    return await user_repo.register_user(user)
