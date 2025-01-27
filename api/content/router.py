from typing import List
from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session
from ..auth.middleware import get_current_user
from ..user.middleware import role_checker
from ..user.models import User, Role

from .schemes import (
    NewContent,
    ContentResponse,
    GetContentFilters,
    ContentUpdateRequest,
)
from . import queries as qr


router = APIRouter(prefix="/content")


@router.get("/categories", response_model=dict)
async def get_categories():
    return await qr.get_categories()


@router.get("/category/{name}", response_model=str)
async def get_category(name: str):
    return await qr.get_category(name)


@router.post("/upload", response_model=ContentResponse)
async def upload_content(
    new_content: NewContent = Depends(),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    await role_checker(current_user, [Role.ADMIN], "only admin can upload content")

    new_content = await qr.create_content(
        session, current_user.id, current_user.username, new_content
    )
    return await new_content.to_pydantic()


@router.get("s/", response_model=List[ContentResponse])
async def get_contents(
    filters: GetContentFilters = Depends(),
    session: AsyncSession = Depends(get_session),
):
    contents = await qr.get_contents(session, filters)
    return contents


@router.get("/{content_id}", response_model=ContentResponse)
async def get_content(
    content_id: int,
    session: AsyncSession = Depends(get_session),
):
    content = await qr.get_content(session, content_id)
    return await content.to_pydantic()


@router.patch("/{content_id}", response_model=ContentResponse)
async def update_content(
    content_id: int,
    update_data: ContentUpdateRequest,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    await role_checker(current_user, [Role.ADMIN], "only admin can upload content")
    updated_content = await qr.update_content(session, content_id, update_data)
    return updated_content


@router.delete("/{content_id}")
async def delete_content(
    content_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    await role_checker(current_user, [Role.ADMIN], "only admin can delete content")
    await qr.delete_content(session, content_id)
    return {"detail": "Content successfully deleted"}
