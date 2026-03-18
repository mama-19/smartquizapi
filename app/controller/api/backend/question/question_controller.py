from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException,Query,Form,status
from typing import Optional,Dict,List
from datetime import datetime,date
import uuid
import json
from app.schemas.question.question_schema import QuestionData , Question as QuestionSchema
from app.models.question.question_model import QuestionType,ActiveStatus,Question as QuestionModel
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
        "question_type": row["question_type"],
        "is_active": ActiveStatus[row["is_active"]].value,
        "created_at": row["created_at"],
        "updated_at": row["updated_at"]
    }

async def list_question(
    db:AsyncSession,
    page:int = 1,
    page_size: int = 10
):
    """ lists question """
    try:
        params = {}
        base_query = f"""
            SELECT * FROM question WHERE 1=1
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
    
async def create_question(
    db:AsyncSession,
    question:QuestionData
):
    try:
        question_data = question.model_dump()
        data = QuestionModel(**question_data)
        db.add(data)
        await db.commit()
        await db.refresh(data)
        return app_success(data=QuestionSchema.model_validate(data))
    except Exception as e:
        return app_server_error(msg=str(e))

async def update_question(
    db:AsyncSession,
    update_question:QuestionData,
    question_id:Optional[int] = None
):
    """ Update question """
    try:
        result = await db.execute(select(QuestionModel).where(QuestionModel.id == question_id))
        question_data = result.scalars().one_or_none()
        if question_data is None:
            return app_error(msg="Question Not Found")
        for field,value in update_question.dict().items():
            if value is not None:
                setattr(question_data,field,value)
        await db.commit()
        await db.refresh(question_data)
        return app_success(data=QuestionSchema.model_validate(question_data))
    except Exception as e:
        return app_server_error(msg=str(e))
    
async def update_question_active_status(
    db:AsyncSession,
    question_id:Optional[int] = None,
    active_status:Optional[ActiveStatus] = None
):
    """ update active status question """
    try:
        result = await db.execute(select(QuestionModel).where(QuestionModel.id == question_id))
        question_data = result.scalars().one_or_none()
        if question_data is None:
            return app_error(msg="Question Not Found")
        question_data.is_active = active_status
        await db.commit()
        await db.refresh(question_data)
        return app_success(data=QuestionSchema.model_validate(question_data))
    except Exception as e:
        return app_server_error(msg=str(e))

async def delete_question(
    db:AsyncSession,
    question_id:Optional[int] = None,
):
    """ Delete  question by id """
    try:
        result = await db.execute(select(QuestionModel).where(QuestionModel.id == question_id))
        question_data = result.scalars().one_or_none()
        if question_data is None:
            return app_error(msg="Question Not Found")
        await db.delete(question_data)
        await db.commit()
        return app_success(data=QuestionSchema.model_validate(question_data))
    except Exception as e:
        return app_server_error(msg=str(e))
    







