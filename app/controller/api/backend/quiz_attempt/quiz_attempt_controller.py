from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from typing import Optional, List, Dict
from datetime import datetime

from app.models.quiz_attempt.quiz_attempt_model import QuizAttempt as QuizAttemptModel
from app.models.quiz_attempt_answer.quiz_attempt_answer_model import QuizAttemptAnswer as QuizAttemptAnswerModel
from app.schemas.quiz_attempt.quiz_attempt_schema import (
    QuizAttempt as QuizAttemptSchema,
    QuizAttemptData,
)
from app.base.untility import app_error, app_success, app_server_error, app_success_paginated, paginate_sql


# ----------------- Quiz Attempt -----------------
async def list_quiz_attempt(
    db: AsyncSession,
    user_id: Optional[int] = None,
    quiz_id: Optional[int] = None,
    page: int = 1,
    page_size: int = 10
):
    """ List all quiz attempts with optional filters """
    try:
        filters = []
        params = {}
        if user_id:
            filters.append("user_id = :user_id")
            params["user_id"] = user_id
        if quiz_id:
            filters.append("quiz_id = :quiz_id")
            params["quiz_id"] = quiz_id
        filter_clause = " AND " + " AND ".join(filters) if filters else ""

        base_query = f"SELECT * FROM quiz_attempt WHERE 1=1 {filter_clause}"
        rows, total_records, total_pages = await paginate_sql(
            db=db,
            full_sql=base_query,
            params=params,
            page=page,
            page_size=page_size
        )
        data = [QuizAttemptSchema.model_validate(row) for row in rows]
        return app_success_paginated(
            total_records=total_records,
            total_pages=total_pages,
            current_page=page,
            page_size=page_size,
            lists=data
        )
    except Exception as e:
        return app_server_error(msg=str(e))


async def create_quiz_attempt(db: AsyncSession, attempt: QuizAttemptData):
    """ Create a new quiz attempt """
    try:
        data = QuizAttemptModel(**attempt.model_dump())
        db.add(data)
        await db.commit()
        await db.refresh(data)
        return app_success(data=QuizAttemptSchema.model_validate(data))
    except Exception as e:
        return app_server_error(msg=str(e))


async def update_quiz_attempt(db: AsyncSession, attempt_id: int, attempt_data: QuizAttemptData):
    """ Update quiz attempt by id """
    try:
        result = await db.execute(select(QuizAttemptModel).where(QuizAttemptModel.id == attempt_id))
        attempt = result.scalars().one_or_none()
        if not attempt:
            return app_error(msg="Quiz attempt not found")
        for field, value in attempt_data.dict().items():
            if value is not None:
                setattr(attempt, field, value)
        await db.commit()
        await db.refresh(attempt)
        return app_success(data=QuizAttemptSchema.model_validate(attempt))
    except Exception as e:
        return app_server_error(msg=str(e))
