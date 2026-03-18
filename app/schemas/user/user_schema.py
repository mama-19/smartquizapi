from fastapi import Form,HTTPException
from pydantic import BaseModel, EmailStr, ConfigDict,Field,validator
from typing import TypeVar, Optional,List
from datetime import datetime
import uuid
import json
from app.models.user.user_model import ActiveStatus,Role
from sqlalchemy.dialects.postgresql import UUID
T = TypeVar("T")

class UserBase(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    role:Optional[Role] = None
    is_active: Optional[ActiveStatus] = None
    password: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class UserData(UserBase):
    @staticmethod
    def as_form(
        username: Optional[str] = Form(None),
        email: Optional[EmailStr] = Form(None),
        role: Optional[Role] = Form(None),
        password: Optional[str] = Form(None),
        is_active: Optional[ActiveStatus] = Form(None),
        created_at: Optional[datetime] = Form(None),
        updated_at: Optional[datetime] = Form(None)
    ):
        return UserData(
            username=username,
            email=email,
            password=password,
            role=role,
            is_active=is_active,
            created_at=created_at,
            updated_at=updated_at
        )
    
class User(UserBase):
    id:int
    model_config = ConfigDict(from_attributes=True)
        