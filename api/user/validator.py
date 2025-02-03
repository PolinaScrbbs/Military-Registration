from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.sql import exists
from sqlalchemy.ext.asyncio import AsyncSession

from .models import User


async def user_exists_by_username(session: AsyncSession, username: str) -> None:
    user_exists = await session.execute(
        select(exists().where(User.username == username))
    )
    if not user_exists.scalar():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with username '{username}' does not exist.",
        )
