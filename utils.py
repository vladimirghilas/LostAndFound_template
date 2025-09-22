from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import Base


async def get_object_or_404(session: AsyncSession, model:Base, item_id:int)-> Base:
    db_item = await session.get(model, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail=F"Object with id={item_id} not found")
    return db_item
