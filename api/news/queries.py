from datetime import datetime
from pathlib import Path
from typing import List, Tuple

from fastapi import UploadFile, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import and_
from sqlalchemy.ext.asyncio import AsyncSession

from ..user.validator import user_exists_by_username

from config import config as conf
from .models import News
from .schemes import NewNews, NewsResponse

# from .validator import CreateContentValidator, UpdateContentValidator


async def create_news(
    session: AsyncSession, new_news_data: NewNews, current_user_id: int
) -> NewsResponse:
    # validator

    new_news = News(
        title=new_news_data.title,
        content=new_news_data.content,
        creator_id=current_user_id,
    )

    session.add(new_news)
    await session.commit()
    await session.refresh(new_news)

    return await new_news.to_pydantic()


async def get_news_list(
    session: AsyncSession, skip: int, limit: int
) -> List[NewsResponse]:
    result = await session.execute(select(News).offset(skip).limit(limit))

    news_list = result.scalars().all()
    pydantic_news_list = [await news.to_pydantic() for news in news_list]
    return pydantic_news_list
