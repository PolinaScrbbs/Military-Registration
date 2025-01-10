from pathlib import Path
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from config import config as conf
from .models import Content, ContentCategory
from .schemes import NewContent
from .validator import CreateContentValidator


async def upload_content(
    session: AsyncSession, file: UploadFile, user_folder: str, category: ContentCategory, filename: str
) -> str:
    original_extension = Path(file.filename).suffix
    validator = CreateContentValidator(
        filename=filename,
        category=category,
        extension=original_extension[1:],
        session=session
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
