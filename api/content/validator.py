import re
from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth.validator import ValidateError
from .models import ContentCategory


class CreateContentValidator:
    def __init__(
        self,
        filename: str,
        category: ContentCategory,
        extension: str,
        session: AsyncSession,
    ) -> None:
        self.filename = filename
        self.category = category
        self.extension = extension
        self.session = session

    async def validate(self):
        try:
            await self.validate_filename()
            await self.validate_extension()
            await self.validate_category()
        except ValidateError as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)

    async def validate_filename(self):
        if not self.filename or self.filename == "":
            raise ValidateError(
                "Filename cannot be empty", status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        if not (4 <= len(self.filename) <= 50):
            raise ValidateError(
                "Filename must be between 4 and 50 characters long",
                status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        if not re.match(r"^[A-Za-z0-9 ]+$", self.filename):
            raise ValidateError(
                "Filename must consist only of English letters, digits, and spaces",
                status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        result = await self.session.execute(
            text(
                f"SELECT 1 FROM contents WHERE filename = :filename AND category = :category"
            ),
            {"filename": self.filename, "category": self.category.name},
        )

        if result.fetchone():
            raise ValidateError(
                "Content with this filename already exists in the selected category. Please choose a different name.",
                status.HTTP_409_CONFLICT,
            )

    async def validate_extension(self):
        if self.extension not in [
            "txt",
            "docx",
            "xlsx",
            "pptx",
            "png",
            "jpeg",
            "jpg",
            "mp4",
        ]:
            raise ValidateError(
                f"Invalid file extension: {self.extension}. "
                "Valid extensions: txt, docx, xlsx, pptx, png, jpeg, jpg, mp4",
                status.HTTP_400_BAD_REQUEST,
            )
        match self.category:
            case ContentCategory.GALLERY:
                if self.extension not in ["png", "jpg", "jpeg"]:
                    raise ValidateError(
                        "Invalid file extension for gallery content. "
                        "Valid extensions: png, jpg, jpeg",
                        status.HTTP_400_BAD_REQUEST,
                    )
            case ContentCategory.STUDENTS:
                if self.extension not in ["docx"]:
                    raise ValidateError(
                        "Invalid file extension for students content. "
                        "Valid extensions: docx",
                        status.HTTP_400_BAD_REQUEST,
                    )
            case (
                ContentCategory.MILITARY_TRAINING_CAMPS
                | ContentCategory.EVENTS
                | ContentCategory.PATRIOTIC_EDUCATION
            ):
                if self.extension not in ["docx", "pptx", "mp4"]:
                    raise ValidateError(
                        f"Invalid file extension for {self.category.value.replace('_', ' ')}. "
                        "Valid extensions: docx, pptx, mp4",
                        status.HTTP_400_BAD_REQUEST,
                    )
            case _:
                if self.extension not in ["txt", "docx", "xlsx", "pptx"]:
                    raise ValidateError(
                        f"Invalid file extension for {self.category.value.replace('_', ' ')}. "
                        "Valid extensions: txt, docx, xlsx, pptx",
                        status.HTTP_400_BAD_REQUEST,
                    )

    async def validate_category(self):
        if self.category not in ContentCategory:
            raise ValidateError("Invalid category", status.HTTP_400_BAD_REQUEST)


class UpdateContentValidator:
    def __init__(
        self,
        content_id: int,
        filename: Optional[str],
        category: Optional[ContentCategory],
        archived: Optional[bool],
        extension: Optional[str],
        session: AsyncSession,
    ) -> None:
        self.content_id = content_id
        self.filename = filename
        self.category = category
        self.archived = archived
        self.extension = extension
        self.session = session

    async def validate(self):
        try:
            if self.filename:
                await self.validate_filename()
            if self.category:
                await self.validate_category()
            if self.archived is not None:
                await self.validate_archived()
            if self.extension and self.category:
                await self.validate_extension()
        except ValidateError as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)

    async def validate_filename(self):
        if self.filename == "":
            raise ValidateError(
                "Filename cannot be empty", status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        if not (4 <= len(self.filename) <= 50):
            raise ValidateError(
                "Filename must be between 4 and 50 characters long",
                status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        if not re.match(r"^[A-Za-z0-9 ]+$", self.filename):
            raise ValidateError(
                "Filename must consist only of English letters, digits, and spaces",
                status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        result = await self.session.execute(
            text(
                f"SELECT 1 FROM contents WHERE filename = :filename AND category = :category AND id != :content_id"
            ),
            {
                "filename": self.filename,
                "category": self.category.name if self.category else None,
                "content_id": self.content_id,
            },
        )

        if result.fetchone():
            raise ValidateError(
                "Content with this filename already exists in the selected category. Please choose a different name.",
                status.HTTP_409_CONFLICT,
            )

    async def validate_category(self):
        if self.category not in ContentCategory:
            raise ValidateError("Invalid category", status.HTTP_400_BAD_REQUEST)

    async def validate_archived(self):
        if not isinstance(self.archived, bool):
            raise ValidateError(
                "Archived must be a boolean value", status.HTTP_422_UNPROCESSABLE_ENTITY
            )

    async def validate_extension(self):
        valid_extensions = {
            ContentCategory.GALLERY: [".png", ".jpg", ".jpeg"],
            ContentCategory.STUDENTS: [".docx"],
            ContentCategory.MILITARY_TRAINING_CAMPS: [".docx", ".pptx", ".mp4"],
            ContentCategory.EVENTS: [".docx", ".pptx", ".mp4"],
            ContentCategory.PATRIOTIC_EDUCATION: [".docx", ".pptx", ".mp4"],
            "default": [".txt", ".docx", ".xlsx", ".pptx"],
        }

        allowed_extensions = valid_extensions.get(
            self.category, valid_extensions["default"]
        )

        if self.extension not in allowed_extensions:
            raise ValidateError(
                f"Invalid file extension for {self.category.value.replace('_', ' ') if self.category else 'selected category'}. "
                f"Valid extensions: {', '.join(allowed_extensions)}",
                status.HTTP_400_BAD_REQUEST,
            )
