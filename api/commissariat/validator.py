import re
from fastapi import HTTPException, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth.validator import ValidateError


class CreateCommissariatValidator:
    def __init__(
        self,
        name: str,
        address: str,
        commissioner_id: int,
        session: AsyncSession,
    ) -> None:
        self.name = name
        self.address = address
        self.commissioner_id = commissioner_id
        self.session = session

    async def validate(self):
        try:
            await self.validate_name()
            await self.validate_address()
            await self.validate_commissioner()
            await self.validate_unique_commissariat()
        except ValidateError as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)

    async def validate_name(self):
        if not self.name or self.name == "":
            raise ValidateError(
                "Name cannot be empty", status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        if not (4 <= len(self.name) <= 100):
            raise ValidateError(
                "Name must be between 4 and 100 characters long",
                status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        if not re.match(r"^[A-Za-z0-9 ]+$", self.name):
            raise ValidateError(
                "Name must consist only of English letters, digits, and spaces",
                status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

    async def validate_address(self):
        if not self.address or self.address == "":
            raise ValidateError(
                "Address cannot be empty", status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        if not (4 <= len(self.address) <= 200):
            raise ValidateError(
                "Address must be between 4 and 200 characters long",
                status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

    async def validate_commissioner(self):
        result = await self.session.execute(
            text("SELECT 1 FROM commissioners WHERE id = :commissioner_id"),
            {"commissioner_id": self.commissioner_id},
        )
        if not result.fetchone():
            raise ValidateError(
                "Commissioner with this ID does not exist.",
                status.HTTP_404_NOT_FOUND,
            )

    async def validate_unique_commissariat(self):
        result = await self.session.execute(
            text(
                "SELECT 1 FROM commissariats WHERE name = :name AND address = :address"
            ),
            {"name": self.name, "address": self.address},
        )
        if result.fetchone():
            raise ValidateError(
                "Commissariat with this name and address already exists. Please choose different values.",
                status.HTTP_409_CONFLICT,
            )

        result_name = await self.session.execute(
            text("SELECT 1 FROM commissariats WHERE name = :name"),
            {"name": self.name},
        )
        if result_name.fetchone():
            raise ValidateError(
                "Commissariat with this name already exists. Please choose a different name.",
                status.HTTP_409_CONFLICT,
            )

        result_address = await self.session.execute(
            text("SELECT 1 FROM commissariats WHERE address = :address"),
            {"address": self.address},
        )
        if result_address.fetchone():
            raise ValidateError(
                "Commissariat with this address already exists. Please choose a different address.",
                status.HTTP_409_CONFLICT,
            )
