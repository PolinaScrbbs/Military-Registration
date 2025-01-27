from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session
from ..user.models import User
from ..user.queries import get_user_by_id
from .queries import get_token


async def verify_token_and_get_user(session: AsyncSession, token: str) -> User:
    token = await get_token(session, token)

    if token is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "token not found")

    await token.verify_token(session, None)
    user = await get_user_by_id(session, token.user_id)

    return user


async def get_current_user(
    session: AsyncSession = Depends(get_session),
    token: str = Depends(OAuth2PasswordBearer(tokenUrl="/auth/login")),
) -> User:
    print(token)
    user = await verify_token_and_get_user(session, token)
    return user