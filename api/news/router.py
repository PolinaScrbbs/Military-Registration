from typing import List
from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session
from ..auth.middleware import get_current_user
from ..user.middleware import role_checker
from ..user.models import User, Role

from .schemes import NewNews, NewsResponse
from . import queries as qr


router = APIRouter(prefix="/news")


@router.post("/", response_model=NewsResponse, status_code=201)
async def create_news(
    new_news_data: NewNews = Depends(),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    await role_checker(current_user, [Role.ADMIN], "only admin can create news")
    new_news = await qr.create_news(session, new_news_data, current_user.id)
    return new_news
