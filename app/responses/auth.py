from typing import Tuple
import aiohttp

from ..config import API_URL


async def login(username: str, password: str) -> Tuple[int, str]:
    async with aiohttp.ClientSession(API_URL) as session:
        data = {"username": username, "password": password}

        async with session.post(f"auth/login", data=data) as response:
            return response.status, await response.json()
