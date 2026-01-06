from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException,Query,Form
from typing import Optional,Dict,List
from datetime import datetime,date
import uuid
import json
from app.schemas.category.category_schema import Category as CategorySchema, CategoryData
from app.models.category.category_model import Category as CategoryModel
from app.base.untility import app_error,app_exception_handler,paginate_sql,app_success,app_server_error,app_success_paginated

def filter(
        name:Optional[str] = None,
)->(str,Dict):
    filters = []
    params = {}
    if name:
        filters.append("name ILIKE :name")
        params["name"] = f"{name}%"
    filter_clause = " AND " + " AND ".join(filters) if filters else ""
    return filter_clause,params 

def data_row(row:Dict) -> Dict:
    return{
        "id": row["id"],
        "name": row["name"],
        "description": row["description"],
        "created_at": row["created_at"],
        "updated_at": row["updated_at"]
    }

async def list_category(
    db:AsyncSession,
    name:Optional[str] = None,
    page:int = 1,
    page_size:int = 10
):
    """ Lists Category """
    try:
        filters, params = filter(name=name)
        base_query = f"""
            SELECT * FROM category WHERE 1=1 
            {filters}
        """
        rows, total_records, total_pages = await paginate_sql(
            db=db,
            full_sql= base_query,
            params=params,
            page=page,
            page_size=page_size
        )
        data = [data_row(row) for row in rows]
        return app_success_paginated(
            total_records=total_records,
            total_pages=total_pages,
            current_page=page,
            page_size=page_size,
            lists=data
        )
    except Exception as e:
        return app_server_error(msg=str(e))
    
async def create_category(
    db:AsyncSession,
    category: CategoryData
):
    """ Create Category """
    try:
        category_data = category.model_dump()
        data = CategoryModel(**category_data)
        db.add(data)
        await db.commit()
        await db.refresh(data)
        return app_success(data=CategorySchema.model_validate(data))
    except Exception as e:
        return app_server_error(msg=str(e))
    
async def update_category(
    db:AsyncSession,
    update_category:CategoryData,
    category_id:Optional[int] = None
):
    
    """ Update category by id """
    try:
        result = await db.execute(select(CategoryModel).where(CategoryModel.id == category_id))
        category_data = result.scalars().one_or_none()
        if category_data is None:
            return app_error(msg="Category Not found")
        for field, value in update_category.dict().items():
            if value is not None:
                setattr(category_data,field,value)
        await db.commit()
        await db.refresh(category_data)
        return app_success(data=CategorySchema.model_validate(category_data))
    except Exception as e:
        return app_error(msg=str(e))

async def delete_category(
    db:AsyncSession,
    category_id: Optional[int] = None
):
    """ Delete Category by id """
    try:
        result = await db.execute(select(CategoryModel).where(CategoryModel.id == category_id))
        data = result.scalars().one_or_none()
        if data is None:
            return app_error(msg="Category not found")
        await db.delete(data)
        await db.commit()
        return app_success(data=CategorySchema.model_validate(data))
    except Exception as e:
        return app_server_error(msg=str(e))
