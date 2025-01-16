from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import Depends
from typing import Optional

from app.models.users import User
from app.database import get_general_session


class UserRepository:
    def __init__(self, session: AsyncSession = Depends(get_general_session)):
        self.session = session

    async def create_user(self, **kwargs) -> User:
        user = User(**kwargs)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_user_by_email(self, email: str) -> Optional[User]:
        user = await self.session.execute(select(User).where(User.email == email))
        return user.scalars().first()

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        return await self.session.get(User, user_id)

    async def update_user(self, user: User) -> User:
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def delete_user(self, user: User):
        await self.session.delete(user)
        await self.session.commit()

    async def list_users(self) -> Sequence[User]:
        from sqlalchemy import select

        result = await self.session.execute(select(User))
        return result.scalars().all()
