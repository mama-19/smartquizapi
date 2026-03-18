from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException,Query,Form,status
from typing import Optional,Dict,List
from datetime import datetime,date
import uuid
import json
from app.models.quiz.quiz_model import Quiz as QuizModel
from app.schemas.quiz.quiz_schema import QuizData,Quiz as QuizSchema
from app.models.quiz.quiz_model import ActiveStatus
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
        "title": row["title"],
        "description": row["description"],
        "time_limit": row["time_limit"],
        "total_question": row["total_question"],
        "category_id": row["category_id"],
        "is_active": ActiveStatus[row["is_active"]].value,
        "created_at": row["created_at"],
        "updated_at": row["updated_at"]
    }

async def list_quiz(
    db:AsyncSession,
    title:Optional[str] = None,
    page:int = 1,
    page_size: int = 10,
):
    try:
        filters,params = filter(title=title)
        base_query = f"""
            SELECT * FROM quiz WHERE 1=1
            {filters}
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

async def create_quiz(
    db:AsyncSession,
    quiz: QuizData
):
    try:
        quiz_data = quiz.model_dump()
        data = QuizModel(**quiz_data)
        db.add(data)
        await db.commit()
        await db.refresh(data)
        return app_success(data=QuizSchema.model_validate(data))
    except Exception as e:
        return app_server_error(msg=str(e))

async def update_quiz(
    db:AsyncSession,
    update_quiz: QuizData,
    quiz_id: Optional[int] = None
):
    try:
        result = await db.execute(select(QuizModel).where(QuizModel.id == quiz_id))
        quiz_data = result.scalars().one_or_none()
        if quiz_data is None:
            return app_error(msg="quiz not found")
        for field,value in update_quiz.dict().items():
            if value:
                setattr(quiz_data,field,value)
        await db.commit()
        await db.refresh(quiz_data)
        return app_success(data=QuizSchema.model_validate(quiz_data))
    except Exception as e:
        return app_server_error(msg=str(e))
    
async def update_quiz_active_status(
    db:AsyncSession,
    active_status:Optional[ActiveStatus] = None,
    quiz_id:Optional[int] = None
):
    """ update quiz active status """
    try:
        result = await db.execute(select(QuizModel).where(QuizModel.id == quiz_id))
        quiz_data = result.scalars().one_or_none()
        if quiz_data is None:
            return app_error(msg="not found")
        quiz_data.is_active = active_status
        await db.commit()
        await db.refresh(quiz_data)
        return app_success(data=QuizSchema.model_validate(quiz_data))
    except Exception as e:
        return app_server_error(msg=str(e))
    
async def delete_quiz(
    db:AsyncSession,
    quiz_id:Optional[int] = None
):
    """ delete quiz by id """
    try:
        result = await db.execute(select(QuizModel).where(QuizModel.id == quiz_id))
        quiz_data = result.scalars().one_or_none()
        if quiz_data is None:
            return app_error(msg="not found")
        await db.delete(quiz_data)
        await db.commit()
        return app_success(data=QuizSchema.model_validate(quiz_data))
    except Exception as e:
        return app_server_error(msg=str(e))




