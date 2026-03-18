from fastapi import Form,HTTPException
from pydantic import BaseModel, EmailStr, ConfigDict,Field,validator
from typing import TypeVar, Optional,List
from datetime import datetime
import uuid
import json
from sqlalchemy.dialects.postgresql import UUID
T = TypeVar("T")

# ---------------- Base ----------------
class QuizAttemptBase(BaseModel):
    user_id: Optional[int] = None
    quiz_id: Optional[int] = None
    score: Optional[int] = 0
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

# ---------------- Input/Output Data ----------------
class QuizAttemptData(QuizAttemptBase):
    @staticmethod
    def as_form(
        user_id: Optional[int] = Form(None),
        quiz_id: Optional[int] = Form(None),
        score: Optional[int] = 0,
        started_at: Optional[datetime] = Form(None),
        completed_at: Optional[datetime] = Form(None)
    ):
        return QuizAttemptData(
            user_id=user_id,
            quiz_id=quiz_id,
            score=score,
            started_at=started_at,
            completed_at=completed_at
        )

# ---------------- Response ----------------
class QuizAttempt(QuizAttemptBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
