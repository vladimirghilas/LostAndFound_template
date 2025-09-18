import schemas
import models
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_session

router = APIRouter()


@router.post("/", response_model=schemas.LostItem)
async def create_lost_item(item: schemas.LostItemCreate, session: AsyncSession = Depends(get_session)):
    db_item = models.LostItem(**item.model_dump())
    session.add(db_item)
    await session.commit()
    await session.refresh(db_item)
    return db_item


@router.get("/", response_model=list[schemas.LostItem])
async def read_lost_items(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(models.LostItem))
    items = result.scalars().all()
    return items


@router.get("/{item_id}", response_model=schemas.LostItem)
async def read_lost_item(item_id: int, session: AsyncSession = Depends(get_session)):
    # TODO: напишите реализацию функции
    raise NotImplementedError("Функция еще не реализована")


@router.get("/search", response_model=list[schemas.LostItem])
async def search_lost_items(query: str, session: AsyncSession = Depends(get_session)):
    """
    Вернет список потерянных предметов, у которых имя, описание или местоположение содержат слово query.
    """
    # TODO: напишите реализацию функции
    raise NotImplementedError("Функция еще не реализована")


@router.put("/{item_id}", response_model=schemas.LostItem)
async def update_lost_item(item_id: int, item: schemas.LostItemUpdate, session: AsyncSession = Depends(get_session)):
    # TODO: доработайте функцию, чтобы все тесты на нее проходили
    db_item = await session.get(models.LostItem, item_id)
    for field, value in item.model_dump(exclude_none=True).items():
        setattr(db_item, field, value)
    await session.commit()
    await session.refresh(db_item)
    return db_item


@router.delete("/{item_id}")
async def delete_lost_item(item_id: int, session: AsyncSession = Depends(get_session)):
    # TODO: напишите реализацию функции
    raise NotImplementedError("Функция еще не реализована")
