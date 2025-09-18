from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import Base


async def get_object_or_404(session: AsyncSession, model: Base, id: int) -> Base:
    db_item = await session.get(model, id)
    if db_item is None:
        raise HTTPException(status_code=404, detail=f"Object with id={id} not found")
    return db_item