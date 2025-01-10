from typing import List

from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session
from ..auth.middleware import get_current_user
from ..user.middleware import role_checker
from ..user.models import User, Role

from .schemes import NewCommissariat, CommissariatResponse
from . import queries as qr

router = APIRouter(prefix="/commissariat")


@router.post("/", response_model=CommissariatResponse)
async def create_commissariat(
    new_commissariat: NewCommissariat = Depends(),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    await role_checker(current_user, [Role.ADMIN], "only admin can upload content")

    new_commissariat = await qr.create_commissariat(session, new_commissariat)

    return await new_commissariat.to_pydantic()


@router.get("s/", response_model=List[CommissariatResponse])
async def get_commissariats(
    session: AsyncSession = Depends(get_session),
):
    commissariats = await qr.get_commissariats(session)
    return commissariats
