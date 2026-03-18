from fastapi import Form,HTTPException
from pydantic import BaseModel, EmailStr, ConfigDict,Field,validator
from typing import TypeVar, Optional,List
from datetime import datetime
import uuid
import json
from app.models.question.question_model import ActiveStatus,QuestionType
from sqlalchemy.dialects.postgresql import UUID
T = TypeVar("T")

class QuestionBase(BaseModel):
    content: Optional[str] = None
    is_active:Optional[ActiveStatus] = None,
    question_type:Optional[QuestionType] = None,
    quiz_id:Optional[int] = None
    point:Optional[int] = None
    created_at:Optional[datetime] = None
    updated_at: Optional[datetime] = None

class QuestionData(QuestionBase):
    @staticmethod
    def as_form(
        content: Optional[str] = Form(None),
        quiz_id: Optional[int] = Form(None),
        point: Optional[int] = Form(None),
        question_type:Optional[QuestionType] = Form(None),
        is_active: Optional[ActiveStatus] = Form(None),
        created_at: Optional[datetime] = Form(None),
        updated_at: Optional[datetime] = Form(None)
    ):
        return QuestionData(
            content=content,
            quiz_id=quiz_id,
            question_type=question_type,
            point=point,
            is_active=is_active,
            created_at=created_at,
            updated_at=updated_at
        )
    
class Question(QuestionBase):
    id:int
    model_config = ConfigDict(from_attributes=True)
