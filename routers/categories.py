from fastapi import APIRouter, Depends, HTTPException
from fastapi.params import Depends
from pydantic import BaseModel
from sqlalchemy.future import select
import schemas
import models
from database import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from services.storages import BaseCRUD
router = APIRouter(prefix='/categories', tags=['Categories'])

@router.get('/', response_model=list[schemas.CategoryRead])
async def get_categories(session: AsyncSession = Depends(get_session)):
    crud = BaseCRUD(models.Category)
    categories = await crud.get_all(session)
    # result = await db.execute(select(models.Category))
    # categories = result.scalars().all()
    return categories

@router.get('/{category_id}', response_model=schemas.CategoryRead)
async def get_category_id(category_id: int, session: AsyncSession = Depends(get_session)):
    crud = BaseCRUD(models.Category)
    category = await crud.get_by_id(session, category_id)
    # result = await db.execute(select(models.Category)
    #                           .options(selectinload(models.Category.lost_items))
    #                           .filter(models.Category.id == category_id))
    # category = result.scalar_one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.post('/', response_model=schemas.CategoryRead)
async def create_category(category: schemas.CategoryCreate, session: AsyncSession = Depends(get_session)):
    crud = BaseCRUD(models.Category)
    db_category = await crud.create(session, category.model_dump())
    # db_category = models.Category(**category.model_dump())
    # db.add(db_category)
    # await db.commit()
    # await db.refresh(db_category)
    return db_category

@router.put('/{category_id}', response_model=schemas.CategoryRead)
async def put_category(category_id: int, category_update: schemas.CategoryUpdate, session: AsyncSession = Depends(get_session)):
    crud = BaseCRUD(models.Category)
    db_category = await crud.update(session, category_id, category_update.model_dump(exclude_unset=True))
    if not db_category:
        raise HTTPException(status_code=404, detail='Category not found')
    # result = await db.execute(select(models.Category).filter(models.Category.id == category_id))
    # db_category = result.scalar_one_or_none()
    # if not db_category:
    #     raise HTTPException(status_code=404, detail='Category not found')
    #
    # for field, value in category_update.model_dump(exclude_unset=True).items():
    #     setattr(db_category, field, value)
    #
    # db.add(db_category)
    # await db.commit()
    # await db.refresh(db_category)
    return db_category

class Message(BaseModel):
    message: str
@router.delete('/{category_id}', response_model=Message)
async def category_delete(category_id: int, session: AsyncSession=Depends(get_session)):
    crud = BaseCRUD(models.Category)
    db_category = await crud.delete(session, category_id)
    # result = await db.execute(select(models.Category).filter(models.Category.id == category_id))
    # db_category = result.scalar_one_or_none()
    if not db_category:
        raise HTTPException(status_code=404, detail='Category not found')
    #
    # await db.delete(db_category)
    # await session.commit()

    return { "message": "Category deleted" }
