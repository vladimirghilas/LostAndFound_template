from fastapi import APIRouter, Depends, HTTPException
from fastapi.params import Depends
from sqlalchemy.future import select
import schemas
import models
from database import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

router = APIRouter(prefix='/categories', tags=['Categories'])

@router.get('/', response_model=list[schemas.CategoryRead])
async def get_categories(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(models.Category))
    categories = result.scalars().all()
    return categories

@router.get('/{category_id}', response_model=schemas.CategoryRead)
async def get_category_id(category_id: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(models.Category)
                              .options(selectinload(models.Category.lost_items))
                              .filter(models.Category.id == category_id))
    category = result.scalar_one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.post('/', response_model=schemas.CategoryRead)
async def create_category(category: schemas.CategoryCreate, db: AsyncSession = Depends(get_session)):
    db_category = models.Category(**category.dict())
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category

@router.put('/{category_id}', response_model=schemas.CategoryRead)
async def put_category(category_id: int, category_update: schemas.CategoryUpdate, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(models.Category).filter(models.Category.id == category_id))
    db_category = result.scalar_one_or_none()
    if not db_category:
        raise HTTPException(status_code=404, detail='Category not found')

    for field, value in category_update.dict(exclude_unset=True).items():
        setattr(db_category, field, value)

    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category

@router.delete('/{category_id}', response_model=schemas.CategoryRead)
async def category_delete(category_id: int, db: AsyncSession=Depends(get_session)):
    result = await db.execute(select(models.Category).filter(models.Category.id == category_id))
    db_category = result.scalar_one_or_none()
    if not db_category:
        raise HTTPException(status_code=404, detail='Category not found')

    await db.delete(db_category)
    await db.commit()

    return {'detail': "Category deleted"}
