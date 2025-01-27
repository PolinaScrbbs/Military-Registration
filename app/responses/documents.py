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


import aiohttp
from typing import Tuple, Optional


async def post_document(
    token: str, filename: str, category: str, file_bytes: bytes, original_filename: str
) -> Tuple[int, Optional[dict]]:
    form_data = aiohttp.FormData()
    form_data.add_field(
        "file",
        file_bytes,
        filename=original_filename,
        content_type="application/octet-stream",
    )

    params = {"filename": filename, "category": category}

    async with aiohttp.ClientSession(API_URL) as session:
        async with session.post(
            "/content/upload",
            headers={"Authorization": f"Bearer {token}"},
            params=params,
            data=form_data,
        ) as response:
            return response.status, await response.json()


async def get_document(document_id: int) -> Tuple[int, Optional[List[dict]]]:
    async with aiohttp.ClientSession(API_URL) as session:
        async with session.get(f"/content/{document_id}") as response:
            return response.status, (
                await response.json() if response.status == 200 else None
            )


async def get_categories() -> Tuple[int, Optional[dict]]:
    async with aiohttp.ClientSession(API_URL) as session:
        async with session.get("/content/categories") as response:
            return response.status, await response.json()


async def get_category(category_name: str) -> Tuple[int, Optional[str]]:
    async with aiohttp.ClientSession(API_URL) as session:
        async with session.get(f"/content/category/{category_name}") as response:
            return response.status, await response.json()


async def update_document(
    token: str, document_id: int, data: dict
) -> Tuple[int, Optional[dict]]:
    async with aiohttp.ClientSession(API_URL) as session:
        async with session.patch(
            f"/content/{document_id}",
            headers={"Authorization": f"Bearer {token}"},
            json=data,
        ) as response:
            return response.status, await response.json()


async def delete_document(token: str, document_id: int) -> Tuple[int, Optional[dict]]:
    async with aiohttp.ClientSession(API_URL) as session:
        async with session.delete(
            f"/content/{document_id}",
            headers={"Authorization": f"Bearer {token}"},
        ) as response:
            return response.status, await response.json()
