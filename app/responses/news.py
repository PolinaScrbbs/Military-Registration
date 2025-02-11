from typing import Tuple, List, Optional

import aiohttp

from ..config import API_URL

async def get_news_list(skip: int = 0, limit: int = 5) -> Tuple[int, Optional[List[dict]]]:
    params = {
        "skip": skip,
        "limit": limit
    }

    async with aiohttp.ClientSession(API_URL) as session:
        async with session.get("/news_list", params=params) as response:
            return response.status, (
                await response.json() if response.status == 200 else None
            )


async def get_news(news_id: int) -> Tuple[int, Optional[dict]]:
    async with aiohttp.ClientSession(API_URL) as session:
        async with session.get(f"/news/{news_id}") as response:
            return response.status, (
                await response.json() if response.status == 200 else None
            )