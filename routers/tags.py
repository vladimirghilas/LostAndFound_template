from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from database import get_session
import models
import schemas
from schemas import TagIds
from services.storages import BaseCRUD
from services.auth import get_current_user

router = APIRouter(dependencies=[Depends(get_current_user)])

@router.post('/', response_model=schemas.TagRead)
async def create_tag(tag: schemas.TagCreate, session: AsyncSession=Depends(get_session)):
    crud = BaseCRUD(models.Tag)
    db_tag = await crud.create(session, tag.model_dump())
    return db_tag

@router.get('/', response_model=list[schemas.TagRead])
async def get_tags(session: AsyncSession=Depends(get_session)):
    crud = BaseCRUD(models.Tag)
    list_tags = await crud.get_all(session)
    return list_tags

@router.get("/{tag_id}", response_model=schemas.TagRead)
async def get_tag_by_id(tag_id: int, session: AsyncSession=Depends(get_session)):
    crud = BaseCRUD(models.Tag)
    db_tag = await crud.get_by_id(session, tag_id)
    if not db_tag:
        raise HTTPException(status_code=404, detail='Tag not found')
    return db_tag

@router.put('/{tag_id}', response_model=schemas.TagRead)
async def update_tag(tag_id: int, update_tag: schemas.TagUpdate, session: AsyncSession=Depends(get_session)):
    crud = BaseCRUD(models.Tag)
    tag = await crud.update(session, tag_id, update_tag.model_dump(exclude_unset=True))
    if not tag:
        raise HTTPException(status_code=404, detail='Tag not found')
    return tag

@router.delete('/{tag_id}', response_model=dict)
async def delete_tag(tag_id: int, session: AsyncSession=Depends(get_session)):
    crud = BaseCRUD(models.Tag)
    result = await crud.delete(session, tag_id)
    if not result:
        raise HTTPException(status_code=404, detail='Tag not found')
    return result

@router.put('/lost/{lost_item_id}', response_model=dict)
async def attash_tags_to_lost_item(
        lost_item_id: int, payload: schemas.TagIds,
        session: AsyncSession=Depends(get_session)):

    result = await session.execute(
        select(models.LostItem)
        .where(models.LostItem.id == lost_item_id)
        .options(selectinload(models.LostItem.tags))
    )
    lost_item_db = result.scalar_one_or_none()
    if not lost_item_db:
        raise HTTPException(status_code=404, detail='Item not found')

    tag_ids = payload.tag_ids
    result = await session.execute(select(models.Tag)
            .where(models.Tag.id.in_(tag_ids)))
    tags = result.scalars().all()

    for tag in tags:
        lost_item_db.tags.append(tag)
    await session.commit()
    return {"success": True}

@router.delete('/{tag_id}/lost/{lost_item_id}', response_model=dict)
async def detash_tag_from_lost_item(tag_id: int, lost_item_id: int, session: AsyncSession=Depends(get_session)):
    tag = await session.get(models.Tag, tag_id)

    if tag is None:
        raise HTTPException(status_code=404, detail='tag not found')

    result= await session.execute(
        select(models.LostItem)
        .where(models.LostItem.id == lost_item_id)
        .options(selectinload(models.LostItem.tags))
                )
    lost_item = result.scalar_one_or_none()

    if lost_item is None:
        raise HTTPException(status_code=404, detail='Item not found')

    if tag in lost_item.tags:
        lost_item.tags.remove(tag)
        await session.commit()

    return {"success": True}

@router.put('/found/{found_item_id}', response_model=dict)
async def attach_tag_to_found_item(
        found_item_id: int,
        payload: TagIds,
        session: AsyncSession=Depends(get_session)):

    result = await session.execute(
        select(models.FoundItem)
        .where(models.FoundItem.id == found_item_id)
        .options(selectinload(models.FoundItem.tags))
    )
    found_item = result.scalar_one_or_none()

    if not found_item:
        raise HTTPException(status_code=404, detail='item not found')

    for tag_id in payload.tag_ids:
        tag = await session.get(models.Tag, tag_id)
        if tag is None:
            raise HTTPException(status_code=404, detail="Tag not found")
        if tag not in found_item.tags:
            found_item.tags.append(tag)

    await session.commit()
    return {"success": True}

@router.delete('/{tag_id}/found/{found_item_id}', response_model=dict)
async def detash_tag_from_found_item(
        tag_id: int, found_item_id: int,
        session: AsyncSession=Depends(get_session)
    ):
    tag = await session.get(models.Tag, tag_id)
    if tag is None:
        raise HTTPException(status_code=404, detail='Tag not found')

    result = await session.execute(
        select(models.FoundItem)
        .where(models.FoundItem.id == found_item_id)
        .options(selectinload(models.FoundItem.tags))
    )
    found_item = result.scalar_one_or_none()

    if found_item is None:
        raise HTTPException(status_code=404, detail='Item not found')

    if tag in found_item.tags:
        found_item.tags.remove(tag)
        await session.commit()

    return {"success": True}


