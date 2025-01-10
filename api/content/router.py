from fastapi import Depends, APIRouter, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session
from ..auth.middleware import get_current_user
from ..user.middleware import role_checker
from ..user.models import User, Role

from .schemes import NewContent, ContentResponse
from . import queries as qr


router = APIRouter(prefix="/content")


@router.post("/upload", response_model=ContentResponse)
async def upload_content(
    new_content: NewContent = Depends(),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    await role_checker(current_user, [Role.ADMIN], "only admin can upload content")

    new_content = await qr.create_content(
        session, current_user.id, current_user.username, new_content
    )
    return await new_content.to_pydantic()
