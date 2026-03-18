from fastapi import Form,HTTPException
from pydantic import BaseModel, EmailStr, ConfigDict,Field,validator
from typing import TypeVar, Optional,List
from datetime import datetime
import uuid
import json
from app.models.quiz.quiz_model import ActiveStatus
from sqlalchemy.dialects.postgresql import UUID
T = TypeVar("T")

class QuizBase(BaseModel):
    title:Optional[str] = None
    description: Optional[str] = None
    is_active:Optional[ActiveStatus] = None
    category_id:Optional[int] = None
    time_limit:Optional[int] = None
    total_question: Optional[int] = None
    created_at:Optional[datetime] = None
    updated_at: Optional[datetime] = None

class QuizData(QuizBase):
    @staticmethod
    def as_form(
        title: Optional[str] = Form(None),
        description: Optional[str] = Form(None),
        category_id: Optional[int] = Form(None),
        time_limit: Optional[int] = Form(None),
        total_question: Optional[int] = Form(None),
        created_at: Optional[datetime] = Form(None),
        updated_at: Optional[datetime] = Form(None)
    ):
        return QuizData(
            title=title,
            description=description,
            category_id=category_id,
            time_limit=time_limit,
            total_question=total_question,
            created_at=created_at,
            updated_at=updated_at
        )
    
class Quiz(QuizBase):
    id:int
    model_config = ConfigDict(from_attributes=True)
