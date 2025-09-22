from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database import get_session
import models
import schemas

router = APIRouter()


@router.post("/", response_model=schemas.CategoryRead)
async def create_category(category: schemas.CategoryCreate, session: AsyncSession = Depends(get_session)):
    db_category = models.Category(**category.model_dump())
    session.add(db_category)
    await session.commit()
    await session.refresh(db_category)
    return db_category


@router.get("/{category_id}", response_model=schemas.CategoryRead)
async def read_category(category_id: int, session: AsyncSession = Depends(get_session)):
    category = await session.execute(select(models.Category).where(models.Category.id == category_id))
    category = category.scalar_one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.put("/{category_id}", response_model=schemas.CategoryRead)
async def update_category(category_id: int, category_update: schemas.CategoryUpdate,
                          session: AsyncSession = Depends(get_session)):
    category = await session.execute(select(models.Category).where(models.Category.id == category_id))
    category = category.scalar_one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    for key, value in category_update.model_dump(exclude_unset=True).items():
        setattr(category, key, value)

    await session.commit()
    await session.refresh(category)
    return category


@router.delete("/{category_id}", response_model=dict)
async def delete_category(category_id: int, session: AsyncSession = Depends(get_session)):
    category = await session.execute(select(models.Category).where(models.Category.id == category_id))
    category = category.scalar_one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    await session.delete(category)
    await session.commit()
    return {"message": "Category deleted"}


# PUT /lost_items/1/category
# body:
# { "category_id": 456 }
#
# PUT /lost_items_category
# body:
# { "category_id": 456, id: 1