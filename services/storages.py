from database import Base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

class BaseCRUD:
    def __init__(self, model: type[Base]):
        self.model = model

    async def get_all(self, session: AsyncSession):
        stmt = select(self.model)
        result = await session.execute(stmt)
        items = result.scalars().all()
        return items

    async def create(self, session: AsyncSession, obj_data: dict):
        db_obj = self.model(**obj_data)
        
