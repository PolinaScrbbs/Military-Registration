from typing import Tuple, List, Optional
import aiohttp

from ..config import API_URL


async def get_documents(category: str) -> Tuple[int, Optional[List[dict]]]:
    async with aiohttp.ClientSession(API_URL) as session:
        async with session.get(f"/contents/?category={category}") as response:
            return response.status, (
                await response.json() if response.status == 200 else None
            )

async def get_archived_documents() -> Tuple[int, Optional[List[dict]]]:
    async with aiohttp.ClientSession(API_URL) as session:
        async with session.get(f"/contents/?archived={True}") as response:
            return response.status, (
                await response.json() if response.status == 200 else None
            )