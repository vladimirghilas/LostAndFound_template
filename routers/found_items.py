import schemas
import models
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db

router = APIRouter()


@router.post("/", response_model=schemas.FoundItem)
async def create_found_item(item: schemas.FoundItemCreate, db: AsyncSession = Depends(get_db)):
    db_item = models.FoundItem(**item.model_dump())
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item


@router.get("/", response_model=list[schemas.FoundItem])
async def read_found_items(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.FoundItem))
    items = result.scalars().all()
    return items


@router.get("/{item_id}", response_model=schemas.FoundItem)
async def read_found_item(item_id: int, db: AsyncSession = Depends(get_db)):
    # TODO: напишите реализацию функции
    raise NotImplementedError("Функция еще не реализована")


@router.put("/{item_id}", response_model=schemas.FoundItem)
async def update_found_item(item_id: int, item: schemas.FoundItemUpdate, db: AsyncSession = Depends(get_db)):
    # TODO: доработайте функцию, чтобы все тесты на нее проходили
    db_item = await db.get(models.FoundItem, item_id)
    for field, value in item.model_dump(exclude_none=True).items():
        setattr(db_item, field, value)
    await db.commit()
    await db.refresh(db_item)
    return db_item


@router.delete("/{item_id}")
async def delete_found_item(item_id: int, db: AsyncSession = Depends(get_db)):
    # TODO: напишите реализацию функции
    raise NotImplementedError("Функция еще не реализована")
