from fastapi import APIRouter, Depends, HTTPException, Query, Form
from sqlalchemy.ext.asyncio import AsyncSession
from app.base.database import get_db
from typing import Optional, Union,List
import uuid 
from app.controller.api.backend.Category.category_controller import (
    list_category,
    create_category,
    delete_category,
    update_category
)
from app.schemas.category.category_schema import CategoryData

router = APIRouter()

""" Category route """
@router.get("/tes")
def func_test():
    return {"Hello": "World"}
@router.get("/smartquizs/category/list")
async def func_list_category(
    db:AsyncSession = Depends(get_db),
    name:Optional[str] = None,
    page:int = 1,
    page_size: int = 10,
):
    return await list_category(
        db=db,
        name=name,
        page=page,
        page_size=page_size
    )
@router.post("/smartquizs/category/create")
async def func_create_category(
    db:AsyncSession = Depends(get_db),
    category: CategoryData = Depends(CategoryData.as_form)
):
    return await create_category(db=db,category=category)

@router.put("/smartquizs/category/update")
async def func_update_category(
    db:AsyncSession = Depends(get_db),
    category_id: Optional[int] = Query(None),
    category: CategoryData = Depends(CategoryData.as_form)
):
    return await update_category(db=db,category_id=category_id,update_category=category)

@router.delete("/smartquizs/category/delete")
async def func_delete_category(
    db:AsyncSession = Depends(get_db),
    category_id:Optional[int] = Query(None)
):
    return await delete_category(db=db,category_id=category_id)