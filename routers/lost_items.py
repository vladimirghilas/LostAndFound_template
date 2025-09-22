from sqlalchemy.orm import selectinload
import schemas
import models
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
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
    result = await session.execute(select(models.LostItem).where(models.LostItem.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="item not found")
    return item


@router.get("/search", response_model=list[schemas.LostItem])
async def search_lost_items(query: str, session: AsyncSession = Depends(get_session)):
    """
    Вернет список потерянных предметов, у которых имя, описание или местоположение содержат слово query.
    """
    # TODO: напишите реализацию функции
    stmt = select(models.LostItem).where(
        or_(
            models.LostItem.name.ilike(f"%{query}%"),
            models.LostItem.description.ilike(f"%{query}%"),
            models.LostItem.location.ilike(f"%{query}%")
        )
    )
    result = await session.execute(stmt)
    items = result.scalars().all()
    return items


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
    db_item = await session.get(models.LostItem, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="iten not found")
    await session.delete(db_item)
    await session.commit()

@router.get('/{item_id}/{category}', response_model=schemas.LostItem)
async def get_lost_item_category(item_id: int, session: AsyncSession=Depends(get_session)):
    query = (
        select(models.LostItem)
        .where(models.LostItem.id == item_id)
        .options(selectinload(models.LostItem.category))
    )
    result = await session.execute(query)
    item = result.scalar_one_or_none()

    if not item:
        raise HTTPException(status_code=404, detail='Item not found')

    if not item.category:
        raise HTTPException(status_code=404, detail="Category not found")

    return schemas.CategoryRead.model_validate(item.category)