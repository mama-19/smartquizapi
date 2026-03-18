from fastapi import Form,HTTPException
from pydantic import BaseModel, EmailStr, ConfigDict,Field,validator
from typing import TypeVar, Optional,List
from datetime import datetime
import uuid
import json
from sqlalchemy.dialects.postgresql import UUID
T = TypeVar("T")
# ---------------- QuizAttemptAnswer ----------------
class QuizAttemptAnswerBase(BaseModel):
    quiz_attempt_id: Optional[int] = None
    question_id: Optional[int] = None
    answer_id: Optional[int] = None
    is_correct: Optional[bool] = None
    answered_at: Optional[datetime] = None

class QuizAttemptAnswerData(QuizAttemptAnswerBase):
    @staticmethod
    def as_form(
        quiz_attempt_id: Optional[int] = Form(None),
        question_id: Optional[int] = Form(None),
        answer_id: Optional[int] = Form(None),
        is_correct: Optional[bool] = Form(None),
        answered_at: Optional[datetime] = Form(None)
    ):
        return QuizAttemptAnswerData(
            quiz_attempt_id=quiz_attempt_id,
            question_id=question_id,
            answer_id=answer_id,
            is_correct=is_correct,
            answered_at=answered_at
        )

class QuizAttemptAnswer(QuizAttemptAnswerBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
