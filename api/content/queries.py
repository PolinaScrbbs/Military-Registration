from pathlib import Path
from typing import List

from fastapi import UploadFile, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import and_
from sqlalchemy.ext.asyncio import AsyncSession

from ..user.validator import user_exists_by_username

from config import config as conf
from .models import Content, ContentCategory
from .schemes import NewContent, ContentResponse, GetContentFilters
from .validator import CreateContentValidator


async def upload_content(
    session: AsyncSession,
    file: UploadFile,
    user_folder: str,
    category: ContentCategory,
    filename: str,
) -> str:
    original_extension = Path(file.filename).suffix
    validator = CreateContentValidator(
        filename=filename,
        category=category,
        extension=original_extension[1:],
        session=session,
    )
    await validator.validate()

    media_root = Path(conf.media_root)
    save_path = media_root / category.value / user_folder
    save_path.mkdir(parents=True, exist_ok=True)

    file_path = save_path / f"{filename}{original_extension}"

    with open(file_path, "wb") as f:
        f.write(await file.read())

    return str(file_path)


async def create_content(
    session: AsyncSession,
    current_user_id: int,
    current_user_username: str,
    new_content: NewContent,
) -> Content:
    path = await upload_content(
        session,
        new_content.file,
        current_user_username,
        new_content.category,
        new_content.filename,
    )

    content = Content(
        filename=new_content.filename,
        category=new_content.category,
        path=path,
        creator_id=current_user_id,
    )

    session.add(content)
    await session.commit()
    await session.refresh(content)

    return content


async def get_contents(
    session: AsyncSession, filters: GetContentFilters
) -> List[ContentResponse]:
    query = select(Content).options(selectinload(Content.creator)).where(Content.is_archived == filters.archived)

    conditions = []
    if filters.category:
        if filters.category not in ContentCategory:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Invalid category: {filters.category}",
            )
        conditions.append(Content.category == filters.category)
    if filters.creator:
        await user_exists_by_username(session, filters.creator)
        conditions.append(Content.creator.has(username=filters.creator))

    if conditions:
        query = query.where(and_(*conditions))

    result = await session.execute(query)

    contents = result.scalars().all()

    if not contents:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No content found"
        )

    contents = [await content.to_pydantic() for content in contents]
    return contents


async def get_content(session: AsyncSession, content_id: int) -> Content:
    query = (
        select(Content)
        .where(Content.id == content_id)
        .options(selectinload(Content.creator))
    )
    result = await session.execute(query)
    content = result.scalar()

    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Content not found"
        )

    return content
