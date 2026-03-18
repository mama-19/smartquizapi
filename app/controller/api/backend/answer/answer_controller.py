from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException,Query,Form,status
from typing import Optional,Dict,List
from datetime import datetime,date
import uuid
import json
from app.schemas.answer.answer_schema import AnswerData,Answer as AnswerSchema
from app.models.answer.answer_model import ActiveStatus, Answer as AnswerModel
from app.base.untility import (
    app_error,
    app_exception_handler
    ,paginate_sql,app_success
    ,app_server_error
    ,app_success_paginated,
    hash_password,
    verify_password,
    AppException,
)

def filter(
    title:Optional[str],
)->(str,Dict):
    filters = []
    params = {}
    if title:
        filters.append("title ILIKE :title")
        params["title"] = f"{title}%"
    filter_clause = " AND " + " ADN ".join(filters) if filters else ""
    return filter_clause,params

def data_row(row:Dict) -> Dict:
    return{
        "id": row["id"],
        "content": row["content"],
        "quiz_id": row["quiz_id"],
        "point": row["point"],
        "answer_type": row["answer_type"],
        "is_active": ActiveStatus[row["is_active"]].value,
        "created_at": row["created_at"],
        "updated_at": row["updated_at"]
    }

async def list_anwser(
    db:AsyncSession,
    page:int = 1,
    page_size: int = 10
):
    """ lists answer """
    try:
        params = {}
        base_query = f"""
            SELECT * FROM answer WHERE 1=1
        """
        rows,total_records,total_pages = await paginate_sql(
            db=db,
            full_sql=base_query,
            page=page,
            page_size=page_size,
            params=params
        )
        data =[ data_row(row) for row in rows]
        return app_success_paginated(
            total_records=total_records,
            total_pages = total_pages,
            current_page=page,
            page_size=page_size,  
            lists=data   
        )
    except Exception as e:
        return app_server_error(msg=str(e))
    
async def create_answer(
    db:AsyncSession,
    answer:AnswerData
):
    try:
        answer_data = answer.model_dump()
        data = AnswerModel(**answer_data)
        db.add(data)
        await db.commit()
        await db.refresh(data)
        return app_success(data=AnswerSchema.model_validate(data))
    except Exception as e:
        return app_server_error(msg=str(e))

async def update_answer(
    db:AsyncSession,
    update_answer:AnswerData,
    answer_id:Optional[int] = None
):
    """ Update answer """
    try:
        result = await db.execute(select(AnswerModel).where(AnswerModel.id == answer_id))
        answer_data = result.scalars().one_or_none()
        if answer_data is None:
            return app_error(msg="Question Not Found")
        for field,value in update_answer.dict().items():
            if value is not None:
                setattr(answer_data,field,value)
        await db.commit()
        await db.refresh(answer_data)
        return app_success(data=AnswerSchema.model_validate(answer_data))
    except Exception as e:
        return app_server_error(msg=str(e))
    
async def update_answer_active_status(
    db:AsyncSession,
    answer_id:Optional[int] = None,
    active_status:Optional[ActiveStatus] = None
):
    """ update active status answer """
    try:
        result = await db.execute(select(AnswerModel).where(AnswerModel.id == answer_id))
        answer_data = result.scalars().one_or_none()
        if answer_data is None:
            return app_error(msg="Question Not Found")
        answer_data.is_active = active_status
        await db.commit()
        await db.refresh(answer_data)
        return app_success(data=AnswerSchema.model_validate(answer_data))
    except Exception as e:
        return app_server_error(msg=str(e))

async def delete_answer(
    db:AsyncSession,
    answer_id:Optional[int] = None,
):
    """ Delete  answer by id """
    try:
        result = await db.execute(select(AnswerModel).where(AnswerModel.id == answer_id))
        answer_data = result.scalars().one_or_none()
        if answer_data is None:
            return app_error(msg="Question Not Found")
        await db.delete(answer_data)
        await db.commit()
        return app_success(data=AnswerSchema.model_validate(answer_data))
    except Exception as e:
        return app_server_error(msg=str(e))
    







