from typing import Tuple, List
import aiohttp

from ..config import API_URL


async def get_documents(category: str) -> Tuple[int, List[dict]]:
    async with aiohttp.ClientSession(API_URL) as session:
        async with session.get(f"/contents/?category={category}") as response:
            return response.status, await response.json()
