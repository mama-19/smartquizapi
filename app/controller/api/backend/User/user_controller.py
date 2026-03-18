from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException,Query,Form,status
from typing import Optional,Dict,List
from datetime import datetime,date
import uuid
import json
from app.schemas.user.user_schema import UserData
from app.schemas.user.user_schema import User as UserSchema
from app.models.user.user_model import User as UserModel
from app.models.user.user_model import ActiveStatus,Role
from app.base.untility import (
    app_error,
    app_exception_handler
    ,paginate_sql,app_success
    ,app_server_error
    ,app_success_paginated,
    hash_password,
    verify_password,
    verify_token,
    AppException,
    create_access_token,
    create_refresh_token
    )
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/smartquizs/auth/login")

def filter(
    name:Optional[str] = None,
    role:Optional[Role] = None,
    is_active: Optional[ActiveStatus] = None
)->(str,Dict):
    filters = []
    params = {}
    if name:
        filters.append("name ILIKE :name")
        params["name"] = f"{name}%"
    if role:
        filters.append("role = :role")
        params["role"] = f"{role.name}"
    if is_active:
        filters.append("is_active = :is_active")
        params["is_active"] = f"{is_active.name}"
    c = " AND " + " AND ".join(filters) if filters else ""
    return filter_clause,params 

def data_row(row:Dict) -> Dict:
    return{
        "id": row["id"],
        "username": row["username"],
        "email": row["email"],
        "password": row["password"],
        "role": Role[row["role"]].value,
        "is_active": ActiveStatus[row["is_active"]].value,
        "created_at": row["created_at"],
        "updated_at": row["updated_at"]
    }

def data_row_token(user, access_token: Optional[str] = None) -> Dict:
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": Role[user.role].value,
        "is_active": ActiveStatus[user.is_active].value,
        "created_at": user.created_at,
        "updated_at": user.updated_at,
        "access_token": access_token
    }

async def list_user(
    db:AsyncSession,
    name:Optional[str] =  None,
    role:Optional[Role] = None,
    is_active: Optional[ActiveStatus] = None,
    page:int = 1,
    page_size: int = 10
):
    """ List User """
    try:
        filters, params = filter(name=name,role=role,is_active=is_active)
        base_query = f'SELECT * FROM "user" WHERE 1=1 {filters}'
        rows, total_records, total_pages = await paginate_sql(
            db=db,
            full_sql= base_query,
            params=params,
            page=page,
            page_size=page_size
        )
        data = [data_row(row) for row in rows]
        return app_success_paginated(
            total_records=total_records,
            total_pages=total_pages,
            current_page=page,
            page_size=page_size,
            lists=data
        )
    except Exception as e:
        return app_server_error(msg=str(e))

async def create_user(
    db:AsyncSession,
    user:UserData
):
    """ Create user """
    try:
        user.password =hash_password(user.password)
        result_user_exists = await db.execute(select(UserModel).where(UserModel.email == user.email))
        user_exists = result_user_exists.scalars().one_or_none()
        if user_exists is not None:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )
        user_data = user.model_dump()
        data = UserModel(**user_data)

        db.add(data)
        await db.commit()
        await db.refresh(data)
        return app_success(data=UserSchema.model_validate(data))
    except HTTPException:
        raise
    except Exception as e:
        return app_server_error(msg=str(e))
    
async def update_user(
    db:AsyncSession,
    update_user: UserData,
    user_id: Optional[int] = None
):
    """ Update user by id """
    try:
        result = await db.execute(select(UserModel).where(UserModel.id == user_id))
        user_data = result.scalars().one_or_none()
        if user_data is None:
            return app_error(msg="User not found")
        if update_user.password:
            user_data.password = hash_password(update_user.password)
        check_user_exist = db.get(update_user.email,None)
        if check_user_exist is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                 detail="User with this email already exist"
            )
        
        update_user_data = update_user.model_dump(exclude={"password"})
        for field,value in update_user_data.items():
            if value:
                setattr(user_data,field,value)
        await db.commit()
        await db.refresh(user_data)
        return app_success(data=UserSchema.model_validate(user_data))
    except HTTPException:
        raise
    except Exception as e:
        return app_server_error(msg=str(e))
    
async def delete_user(
    db:AsyncSession,
    user_id: Optional[int] = None
):
    """ Delete User By id """
    try:
        resutl = await db.execute(select(UserModel).where(UserModel.id == user_id))
        user_data = resutl.scalars().one_or_none()
        if user_data is None:
            return app_error(msg="user not found")
        await db.delete(user_data)
        await db.commit()
        return app_success(data=UserSchema.model_validate(user_data))
    except Exception as e:
        return app_server_error(msg=str(e))

async def login(
    db:AsyncSession,
    user_form: OAuth2PasswordRequestForm,
):
    """ login with auth2 jwt """
    try:
        resutl = await db.execute(select(UserModel).where(UserModel.username == user_form.username))
        user = resutl.scalars().one_or_none()
        if not user or not verify_password(user_form.password,user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="invalid username or password"
            )
        token_data = {
            "sub": str(user.id),
            "username": user.username,
            "role": user.role.value}
        access_token = create_access_token(token_data)
        return {
            "message": "login success",
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "username": user.username,
                "role": user.role.value
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        return app_server_error(msg=str(e))
    
async def get_current_user(
    db: AsyncSession,
    username:Optional[str] = None
):
    """ get current user"""
    try:
        result = await db.execute(select(UserModel).where(UserModel.username == username))
        user_data = result.scalars().one_or_none()
        if user_data is None:
            return app_error(msg="user not found")
        return app_success(data=UserSchema.model_validate(user_data),msg=user_data)
    except Exception as e:
        return app_server_error(msg=str(e))

