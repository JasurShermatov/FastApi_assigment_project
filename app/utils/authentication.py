from jose import jwt, JWTError
from datetime import timedelta, datetime
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

from app.repositories.users import UserRepository
from app.settings import Settings, get_settings


def create_access_token(
    data: dict, secret_key: str, algorithm: str = "HS256", expires_minutes: int = 60
) -> str:
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, secret_key, algorithm=algorithm)


def decode_token(token: str, secret_key: str, algorithm: str = "HS256") -> dict:
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        return payload
    except JWTError:
        return {}


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    settings: Settings = Depends(get_settings),
    user_repo: UserRepository = Depends(),
):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email = payload.get("email")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token: missing email")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = await user_repo.get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user
