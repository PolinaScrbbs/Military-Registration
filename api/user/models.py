import uuid
from enum import Enum as baseEnum
from typing import Optional
import jwt
import bcrypt
import pytz
from datetime import datetime, timedelta
from sqlalchemy import Column, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from config import config as conf
from ..database import Base


class BaseEnum(baseEnum):
    @classmethod
    async def values(cls):
        return [member.value for member in cls]


class Role(BaseEnum):
    ADMIN = "administrator"
    USER = "user"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True, nullable=False)
    hashed_password = Column(String(512), nullable=False)
    full_name = Column(String(50), nullable=False)
    role = Column(Enum(Role), default=Role.USER, nullable=False)

    contents = relationship("Content", back_populates="creator")

    async def set_password(self, password: str) -> None:
        self.hashed_password = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

    async def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(
            password.encode("utf-8"), self.hashed_password.encode("utf-8")
        )

    async def generate_token(self, token_lifetime: int = conf.token_lifetime) -> str:
        payload = {
            "identity": self.id,
            "exp": datetime.now(pytz.timezone("Europe/Moscow"))
            + timedelta(seconds=token_lifetime),
            "csrf": str(uuid.uuid4()),
        }
        return jwt.encode(payload, conf.secret_key, algorithm="HS256")

    async def format_full_name_to_initials(self) -> str:
        name_parts = self.full_name.split()

        if len(name_parts) < 2:
            return self.full_name

        last_name = name_parts[0]
        initials = "".join([part[0].upper() + "." for part in name_parts[1:]])

        return f"{last_name} {initials}"

    async def to_base_user(self):
        return {
            "id": self.id,
            "username": self.username,
            "full_name": await self.format_full_name_to_initials(),
            "role": "Администратор" if self.role == Role.ADMIN else "Пользователь",
        }


class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True)
    token = Column(String(256), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    async def verify_token(self, session: AsyncSession, user: Optional[User]):
        try:
            jwt.decode(self.token, conf.secret_key, algorithms=["HS256"])
            return status.HTTP_200_OK, "token verification", self

        except jwt.ExpiredSignatureError:
            return await self.refresh_token(session, user)

        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="token is invalid",
                headers={"WWW-Authenticate": "Bearer"},
            )

    async def refresh_token(self, session: AsyncSession, user: Optional[User]):
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )

        new_token = await user.generate_token()

        self.token = new_token
        session.add(self)
        await session.commit()

        return status.HTTP_200_OK, "token updated", self
