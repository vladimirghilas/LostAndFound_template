import schemas
import models
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_session
from utils import get_object_or_404
from services.storages import BaseCRUD

router = APIRouter()


@router.post("/", response_model=schemas.FoundItem)
async def create_found_item(item: schemas.FoundItemCreate, session: AsyncSession = Depends(get_session)):
    db_item = models.FoundItem(**item.model_dump())
    session.add(db_item)
    await session.commit()
    await session.refresh(db_item)
    return db_item


@router.get("/", response_model=list[schemas.FoundItem])
async def read_found_items(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(models.FoundItem))
    items = result.scalars().all()
    return items


@router.get("/{item_id}", response_model=schemas.FoundItem)
async def read_found_item(item_id: int, session: AsyncSession = Depends(get_session)):
    # TODO: напишите реализацию функции
    # result = await session.execute(select(models.FoundItem).where(models.FoundItem.id == item_id))
    # item = result.scalar_one_or_none()
    # if item is None:
    #     raise HTTPException(status_code=404, detail="Item not found")
    item = await get_object_or_404(session, models.FoundItem, item_id)
    return item


@router.put("/{item_id}", response_model=schemas.FoundItem)
async def update_found_item(item_id: int, item: schemas.FoundItemUpdate, session: AsyncSession = Depends(get_session)):
    # TODO: доработайте функцию, чтобы все тесты на нее проходили
    db_item = await get_object_or_404(session, models.FoundItem, item_id)
    for field, value in item.model_dump(exclude_none=True).items():
        setattr(db_item, field, value)
    await session.commit()
    await session.refresh(db_item)
    return db_item


@router.delete("/{item_id}")
async def delete_found_item(item_id: int, session: AsyncSession = Depends(get_session)):
    # TODO: напишите реализацию функции
    item = await session.get(models.FoundItem, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    await session.delete(item)
    await session.commit()
    return {"detail": f"item {item} deleted succesfully"}
