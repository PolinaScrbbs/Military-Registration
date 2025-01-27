from typing import List
from fastapi import HTTPException, status

from .models import User, Role


async def role_checker(
    user: User,
    role: List[Role],
    msg: str,
    status_code: status = status.HTTP_403_FORBIDDEN,
) -> None:
    if user.role not in role:
        raise HTTPException(status_code, msg)