from fastapi import HTTPException, status
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession


from .models import User


async def get_user_by_username(session: AsyncSession, username: str) -> User:

    result = await session.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="user not found")

    return user


async def get_user_by_id(session: AsyncSession, user_id: int) -> User:
    result = await session.execute(select(User).where(User.id == user_id))

    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="user not found")

    return user