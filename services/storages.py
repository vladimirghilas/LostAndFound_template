from collections.abc import Sequence

from fastapi.params import Depends
from watchfiles import awatch

from database import Base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from services.auth import get_password_hash


class BaseCRUD:
    def __init__(self, model: type[Base]):
        self.model = model

    async def get_all(self, session: AsyncSession, skip: int = 0, limit: int = 20) -> Sequence[Base]:
        stmt = select(self.model).offset(skip).limit(limit)
        results = await session.execute(stmt)
        items = results.scalars().all()
        return items

    async def create(self, session: AsyncSession, obj_data: dict) -> Base:
        db_obj = self.model(**obj_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def get_by_id(self, session: AsyncSession, obj_id: int) -> Base | None:
        stmt = select(self.model).where(self.model.id == obj_id)
        result = await session.execute(stmt)
        object = result.scalar_one_or_none()
        return object

    async def update(self, session: AsyncSession, obj_id: int, new_obj_data: dict) -> type[Base] | None:
        db_obj = await session.get(self.model, obj_id)
        if db_obj is None:
            return None
        for field, value in new_obj_data.items():
            setattr(db_obj, field, value)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def delete(self, session: AsyncSession, obj_id: int) -> str | None:
        result = await session.get(self.model, obj_id)
        if not result:
            return None
        await session.delete(result)
        await session.commit()
        return "ok"

    async def create_user(self, session: AsyncSession, user_data: dict) -> Base | None:
        """
                Создаёт пользователя с хэшированием пароля.
                user_data: dict с ключами 'username', 'email', 'full_name', 'password', 'is_active'
                """
        if "password" not in user_data:
            raise ValueError("Password is required")

        hashed_password=get_password_hash(user_data.pop("password"))
        user_data["hashed_password"]=hashed_password

        return await self.create(session=session, obj_data=user_data)


