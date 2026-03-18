from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from typing import Optional, List, Dict
from datetime import datetime
from app.models.quiz_attempt_answer.quiz_attempt_answer_model import QuizAttemptAnswer as QuizAttemptAnswerModel
from app.schemas.quiz_attempt_answer.quiz_attempt_answer_schema import QuizAttemptAnswerData , QuizAttemptAnswer as QuizAttemptAnswerSchema
from app.base.untility import app_error, app_success, app_server_error, app_success_paginated, paginate_sql

async def create_quiz_attempt_answer(db: AsyncSession, answer: QuizAttemptAnswerData):
    """ Record an answer for a quiz attempt """
    try:
        data = QuizAttemptAnswerModel(**answer.model_dump())
        db.add(data)
        await db.commit()
        await db.refresh(data)
        return app_success(data=QuizAttemptAnswerSchema.model_validate(data))
    except Exception as e:
        return app_server_error(msg=str(e))


async def list_quiz_attempt_answer(db: AsyncSession, quiz_attempt_id: Optional[int] = None):
    """ List all answers for a specific quiz attempt """
    try:
        filters = []
        params = {}
        if quiz_attempt_id:
            filters.append("quiz_attempt_id = :quiz_attempt_id")
            params["quiz_attempt_id"] = quiz_attempt_id
        filter_clause = " AND " + " AND ".join(filters) if filters else ""
        base_query = f"SELECT * FROM quiz_attempt_answer WHERE 1=1 {filter_clause}"

        rows, total_records, total_pages = await paginate_sql(
            db=db,
            full_sql=base_query,
            params=params,
            page=1,
            page_size=50  # return all by default
        )
        data = [QuizAttemptAnswerSchema.model_validate(row) for row in rows]
        return app_success_paginated(
            total_records=total_records,
            total_pages=total_pages,
            current_page=1,
            page_size=50,
            lists=data
        )
    except Exception as e:
        return app_server_error(msg=str(e))
