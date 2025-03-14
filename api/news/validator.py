import re
from fastapi import HTTPException, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..auth.validator import ValidateError
from .models import News
from .schemes import NewsUpdateRequest


class CreateNewsValidator:
    def __init__(self, title: str, content: str, session: AsyncSession) -> None:
        self.title = title
        self.content = content
        self.session = session

    async def validate(self):
        try:
            await self.validate_title()
            await self.validate_content()
        except ValidateError as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)

    async def validate_title(self):
        if not self.title or self.title.strip() == "":
            raise ValidateError(
                "Title cannot be empty", status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        if not (4 <= len(self.title) <= 32):
            raise ValidateError(
                "Title must be between 4 and 32 characters long",
                status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        if not re.match(r"^[A-Za-z0-9 ]+$", self.title):
            raise ValidateError(
                "Title must consist only of English letters, digits, and spaces",
                status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        result = await self.session.execute(
            text("SELECT 1 FROM news WHERE title = :title"),
            {"title": self.title},
        )

        if result.fetchone():
            raise ValidateError(
                "A news article with this title already exists. Please choose a different title.",
                status.HTTP_409_CONFLICT,
            )

    async def validate_content(self):
        if not self.content or self.content.strip() == "":
            raise ValidateError(
                "Content cannot be empty", status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        if len(self.content) > 128:
            raise ValidateError(
                "Content must not exceed 128 characters",
                status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        if not re.match(r"^[A-Za-z0-9 .,!?;:'\"()-]+$", self.content):
            raise ValidateError(
                "Content must consist only of English letters, digits, and punctuation marks",
                status.HTTP_422_UNPROCESSABLE_ENTITY,
            )


class UpdateNewsValidator:
    def __init__(
        self, news_id: int, update_data: NewsUpdateRequest, session: AsyncSession
    ) -> None:
        self.news_id = news_id
        self.title = update_data.title
        self.content = update_data.content
        self.session = session

    async def validate(self):
        try:
            if self.title:
                await self.validate_title()
            if self.content:
                await self.validate_content()
        except ValidateError as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)

    async def validate_title(self):
        if not self.title or len(self.title) < 5 or len(self.title) > 32:
            raise ValidateError(
                "Title must be between 5 and 32 characters long",
                status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        if not re.match(r"^[A-Za-z0-9 ]+$", self.title):
            raise ValidateError(
                "Title must consist only of English letters, digits, and spaces",
                status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        result = await self.session.execute(
            select(News.id).where(News.title == self.title, News.id != self.news_id)
        )
        if result.scalar():
            raise ValidateError(
                "A news item with this title already exists. Please choose another title.",
                status.HTTP_409_CONFLICT,
            )

    async def validate_content(self):
        if not self.content or len(self.content) < 10 or len(self.content) > 128:
            raise ValidateError(
                "Content must be between 10 and 128 characters long",
                status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        if not re.match(r"^[A-Za-z0-9 .,!?;:'\"()-]+$", self.content):
            raise ValidateError(
                "Content must consist only of English letters, digits, and punctuation marks",
                status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
