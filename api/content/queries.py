from pathlib import Path
from fastapi import HTTPException, status, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from config import config as conf
from .models import Content
from .schemes import NewContent


async def file_type_checker(file) -> None:
    ALLOWED_MIME_TYPES = {
        "txt": "text/plain",
        "word": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "excel": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "png": "image/png",
        "jpeg": "image/jpeg",
        "powerpoint": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    }

    if file.content_type not in ALLOWED_MIME_TYPES.values():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type: {file.content_type}. "
            f"Valid types: {', '.join(ALLOWED_MIME_TYPES.keys())}",
        )


async def upload_content(
    file: UploadFile, user_folder: str, category: str, filename: str
) -> str:
    media_root = Path(conf.media_root)
    save_path = media_root / category / user_folder
    save_path.mkdir(parents=True, exist_ok=True)

    original_extension = Path(file.filename).suffix
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
        new_content.file,
        current_user_username,
        new_content.category.value,
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
