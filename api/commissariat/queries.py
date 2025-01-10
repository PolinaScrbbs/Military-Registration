from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Commissariat
from .schemes import NewCommissariat


async def create_commissariat(
    session: AsyncSession, new_commissariat=NewCommissariat
) -> Commissariat:
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
