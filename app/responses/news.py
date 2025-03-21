from typing import Tuple, List, Optional

import aiohttp

from ..config import API_URL


async def get_news_list(
    skip: int = 0, limit: int = 5
) -> Tuple[int, Optional[List[dict]]]:
    params = {"skip": skip, "limit": limit}

    async with aiohttp.ClientSession(API_URL) as session:
        async with session.get("/news_list", params=params) as response:
            return response.status, (
                await response.json() if response.status == 200 else None
            )


async def post_news(token: str, title: str, content: str) -> Tuple[int, Optional[dict]]:
    payload  = {"title": title, "content": content}

    async with aiohttp.ClientSession(API_URL) as session:
        async with session.post(
            "/news",
            headers={"Authorization": f"Bearer {token}"},
            json=payload,
        ) as response:
            return response.status, await response.json()


async def get_news(news_id: int) -> Tuple[int, Optional[dict]]:
    async with aiohttp.ClientSession(API_URL) as session:
        async with session.get(f"/news/{news_id}") as response:
            return response.status, (
                await response.json() if response.status == 200 else None
            )


async def update_news(
    token: str, news_id: int, data: dict
) -> Tuple[int, Optional[dict]]:
    async with aiohttp.ClientSession(API_URL) as session:
        async with session.patch(
            f"/news/{news_id}",
            headers={"Authorization": f"Bearer {token}"},
            json=data,
        ) as response:
            return response.status, await response.json()


async def delete_news(token: str, news_id: int) -> Tuple[int, Optional[dict]]:
    async with aiohttp.ClientSession(API_URL) as session:
        async with session.delete(
            f"/news/{news_id}",
            headers={"Authorization": f"Bearer {token}"},
        ) as response:
            return response.status, await response.json()
