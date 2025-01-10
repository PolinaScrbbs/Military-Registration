from typing import List

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Commissariat
from .schemes import NewCommissariat, CommissariatResponse
from .validator import CreateCommissariatValidator


async def create_commissariat(
    session: AsyncSession, new_commissariat=NewCommissariat
) -> Commissariat:
    await CreateCommissariatValidator(
        new_commissariat.name,
        new_commissariat.address,
        new_commissariat.commissioner_id,
        session,
    ).validate()

    commissariat = Commissariat(
        name=new_commissariat.name,
        address=new_commissariat.address,
        commissioner_id=new_commissariat.commissioner_id,
    )

    session.add(commissariat)
    await session.commit()
    await session.refresh(commissariat)

    commissariat_with_commissioner = await session.execute(
        select(Commissariat)
        .options(
            selectinload(Commissariat.commissioner),
            selectinload(Commissariat.phones),
            selectinload(Commissariat.urls),
        )
        .where(Commissariat.id == commissariat.id)
    )

    commissariat = commissariat_with_commissioner.scalars().first()

    return commissariat


async def get_commissariats(session: AsyncSession) -> List[CommissariatResponse]:
    result = await session.execute(
        select(Commissariat).options(
            selectinload(Commissariat.commissioner),
            selectinload(Commissariat.phones),
            selectinload(Commissariat.urls),
        )
    )

    commissariats = result.scalars().all()

    if not commissariats:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No commissariats found"
        )

    return [await commissariat.to_pydantic() for commissariat in commissariats]
