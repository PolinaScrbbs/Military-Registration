from typing import Tuple

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session
from ..user.queries import get_user_by_username, get_user_by_id
from ..user.models import User, Token
from ..user.schemes import UserCreate, BaseUser


async def registration_user(session: AsyncSession, user_create: UserCreate) -> BaseUser:

    user = User(username=user_create.username, full_name=user_create.full_name)
    await user.set_password(user_create.password)
    session.add(user)
    await session.commit()
    await session.refresh(user)

    return BaseUser(
        id=user.id,
        username=user.username,
        role=user.role.value,
        full_name=user.full_name,
    )


async def get_user_token(session: AsyncSession, user_id: int):
    result = await session.execute(select(Token).where(Token.user_id == user_id))

    return result.scalar_one_or_none()


async def login(
    session: AsyncSession, username: str, password: str
) -> Tuple[int, str, str]:

    user = await get_user_by_username(session, username)

    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "user not found")

    correct_password = await user.check_password(password)

    if not correct_password:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, detail="password is incorrect"
        )

    token = await get_user_token(session, user.id)

    if token is None:
        token = await user.generate_token()
        token = Token(user_id=user.id, token=token)
        status_code = status.HTTP_201_CREATED
        msg = "token created"

        session.add(token)
        await session.commit()

    else:
        status_code, msg, token = await token.verify_token(session, user)

    return status_code, msg, token.token


async def get_token(session: AsyncSession, token: str) -> Token:
    result = await session.execute(select(Token).where(Token.token == token))

    return result.scalar_one_or_none()
