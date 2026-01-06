from fastapi import Form,HTTPException
from pydantic import BaseModel, EmailStr, ConfigDict,Field,validator
from typing import TypeVar, Optional,List
from datetime import datetime
import uuid
import json
from sqlalchemy.dialects.postgresql import UUID
T = TypeVar("T")

class CategoryBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class CategoryData(CategoryBase):
    @staticmethod
    def as_form(
        name:Optional[str] = Form(None),
        descripton: Optional[str] = Form(None),
        created_at: Optional[datetime] = Form(None),
        updated_at: Optional[datetime] = Form(None)
    ):
        return CategoryData(
            name=name,
            description=descripton,
            created_at=created_at,
            updated_at=updated_at
        )
    
class Category(CategoryBase):
    id:int
    model_config = ConfigDict(from_attributes=True)
