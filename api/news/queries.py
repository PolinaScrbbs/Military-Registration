from datetime import datetime
from typing import List

from fastapi import HTTPException, status
from sqlalchemy import select, desc
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from .models import News
from .schemes import NewNews, NewsResponse, NewsUpdateRequest

from .validator import CreateNewsValidator, UpdateNewsValidator


async def create_news(
    session: AsyncSession, new_news_data: NewNews, current_user_id: int
) -> NewsResponse:
    validator = CreateNewsValidator(
        title=new_news_data.title,
        content=new_news_data.content,
        session=session,
    )
    await validator.validate()

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
    result = await session.execute(
        select(News)
        .options(selectinload(News.creator))
        .order_by(desc(News.last_updated_at).nullslast(), desc(News.created_at))
        .offset(skip)
        .limit(limit)
    )

    news_list = result.scalars().all()
    pydantic_news_list = [await news.to_pydantic() for news in news_list]
    return pydantic_news_list


async def get_news(session: AsyncSession, news_id: int) -> News:
    result = await session.execute(
        select(News).options(selectinload(News.creator)).where(News.id == news_id)
    )

    news = result.scalar_one_or_none()
    if not news:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="news not found"
        )

    return news


async def update_news(
    session: AsyncSession, news_id: int, update_data: NewsUpdateRequest
) -> NewsResponse:
    validator = UpdateNewsValidator(news_id, update_data, session)
    await validator.validate()

    news = await get_news(session, news_id)

    if update_data.title:
        news.title = update_data.title
    if update_data.content:
        news.content = update_data.content
    news.last_updated_at = datetime.now()

    await session.commit()
    return await news.to_pydantic()


async def delete_news(
    session: AsyncSession,
    news_id: int,
) -> None:
    result = await session.execute(select(News).where(News.id == news_id))
    news = result.scalar_one_or_none()
    if not news:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="news not found"
        )
    await session.delete(news)
    await session.commit()
