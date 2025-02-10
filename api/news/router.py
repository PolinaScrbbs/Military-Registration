from typing import List, Optional
from fastapi import Depends, APIRouter, Query
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session
from ..auth.middleware import get_current_user
from ..user.middleware import role_checker
from ..user.models import User, Role

from .schemes import NewNews, NewsResponse, NewsUpdateRequest
from . import queries as qr


router = APIRouter(prefix="/news")


@router.post("", response_model=NewsResponse, status_code=201)
async def create_news(
    new_news_data: NewNews = Depends(),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    await role_checker(current_user, [Role.ADMIN], "only admin can create news")
    new_news = await qr.create_news(session, new_news_data, current_user.id)
    return new_news


@router.get(path="_list", response_model=List[NewsResponse])
async def get_news_list(
    skip: Optional[int] = Query(0, ge=0, description="Сколько записей пропустить"),
    limit: Optional[int] = Query(
        10, le=100, description="Максимальное количество записей"
    ),
    session: AsyncSession = Depends(get_session),
):
    news_list = await qr.get_news_list(session, skip, limit)
    return news_list


@router.get(path="/{news_id}", response_model=NewsResponse)
async def get_news(
    news_id: int,
    session: AsyncSession = Depends(get_session),
):
    news = await qr.get_news(session, news_id)
    return await news.to_pydantic()


@router.patch("/{news_id}", response_model=NewsResponse)
async def update_news(
    news_id: int,
    news_update_data: NewsUpdateRequest = Depends(),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    await role_checker(current_user, [Role.ADMIN], "only admin can update news")
    updated_news = await qr.update_news(session, news_id, news_update_data)
    return updated_news


@router.delete("/{news_id}")
async def delete_news(
    news_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    await role_checker(current_user, [Role.ADMIN], "only admin can delete news")
    await qr.delete_news(session, news_id)
    return "news has deleted"
