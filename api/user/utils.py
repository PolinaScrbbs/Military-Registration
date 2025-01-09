from fastapi import HTTPException, status
from sqlalchemy.sql import select, exists
from sqlalchemy.ext.asyncio import AsyncSession

from .models import User


async def user_exists_by_id(
    session: AsyncSession, user_id: int, msg: str = "user not found"
) -> None:
    result = await session.execute(select(exists().where(User.id == user_id)))
    user_exists = result.scalar()

    if not user_exists:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=msg)


async def user_exists_by_username(session: AsyncSession, username: str) -> bool:
    result = await session.execute(select(exists().where(User.username == username)))
    return result.scalar()
