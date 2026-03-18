from fastapi import Form,HTTPException
from pydantic import BaseModel, EmailStr, ConfigDict,Field,validator
from typing import TypeVar, Optional,List
from datetime import datetime
import uuid
import json
from app.models.answer.answer_model import ActiveStatus
from sqlalchemy.dialects.postgresql import UUID
T = TypeVar("T")

class AnswerBase(BaseModel):
    content: Optional[str] = None
    is_active:Optional[ActiveStatus] = None,
    question_id:Optional[int] = None
    is_correct:Optional[bool] = None
    created_at:Optional[datetime] = None
    updated_at: Optional[datetime] = None

class AnswerData(AnswerBase):
    @staticmethod
    def as_form(
        content: Optional[str] = Form(None),
        question_id: Optional[int] = Form(None),
        is_correct: Optional[bool] = Form(None),
        is_active: Optional[ActiveStatus] = Form(None),
        created_at: Optional[datetime] = Form(None),
        updated_at: Optional[datetime] = Form(None)
    ):
        return AnswerData(
            content=content,
            question_id=question_id,
            is_correct=is_correct,
            is_active=is_active,
            created_at=created_at,
            updated_at=updated_at
        )
    
class Answer(AnswerBase):
    id:int
    model_config = ConfigDict(from_attributes=True)
