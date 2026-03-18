import uuid
import pytz
from enum import Enum
from typing import Any, List, Optional, Dict, Tuple
from zoneinfo import ZoneInfo
from fastapi import Depends, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Generic, TypeVar
from pydantic import BaseModel
from sqlalchemy.sql import text
import bcrypt
from app.base.database import get_db
from zoneinfo import ZoneInfo
from datetime import datetime, time,timedelta
from fastapi import Depends, HTTPException, Request,status
from fastapi.responses import JSONResponse
from sqlalchemy import event
from fastapi.responses import StreamingResponse
from io import BytesIO
from jose import jwt,JWTError

T = TypeVar("T")
ACCESS_TOKEN_EXPIRES_MINUTES=30 * 24 * 60 # 3day
REFRESH_TOKEN_EXPIRES_MINUTES=5 * 24 * 60  # 5 day
REFRESH_TOKEN_ROTATION=True
ALGORITHM = "HS256"
SECRET_KEY='eyJhbGciO/iJIUzI1N!iIsInR5cCI6Ik/ss=pXVCJ9wertyuiasdfghjklzxcvbnm'
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/smartquizs/auth/login")
class AppSuccessResponse(BaseModel, Generic[T]):
    code: int = 200
    msg: str = "Success"
    data: T
    """    A generic class for success responses.
    Attributes:
        code: HTTP status code (default 200)
        msg: Response message
        data: Response data
    """

def get_date_time_formatted(dt: datetime) -> str:
    """
    Format a datetime object to 'Month Day Year : minute hour' 
    """
    return dt.strftime("%d %b %Y %I:%M %p")

class Role(str,Enum):
    admin = "admin"
    user = "user"


async def paginate_sql(
    db: AsyncSession,
    full_sql: str,
    params: Dict,
    page: int,
    page_size: int
):
    offset = (page - 1) * page_size
    count_sql = f"SELECT COUNT(*) FROM ({full_sql}) AS count_subquery"
    count_result = await db.execute(text(count_sql), params)
    total_records = count_result.scalar_one()
    paginated_sql = f"{full_sql} OFFSET :offset LIMIT :limit"
    params.update({"offset": offset, "limit": page_size})
    result = await db.execute(text(paginated_sql), params)
    rows = result.mappings().all()
    total_pages = (total_records + page_size - 1) // page_size
    return rows, total_records, total_pages

async def paginate(
    db: AsyncSession,
    model: Any,
    filters: List[Any],
    page: int = 1,
    page_size: int = 10
) -> Tuple[List[Any], int, int]:
    """
    Reusable pagination function.

    Args:
        db: AsyncSession model
        model: SQLAlchemy ORM model class
        filters: List of filter expressions
        page: Current page number (1-based)
        page_size: Number of items per page

    Returns:
        Tuple containing:
            - List of model models for the current page
            - Total number of matching records
            - Total number of pages
    """
    count_query = select(func.count()).select_from(model).where(*filters)
    total_records_result = await db.execute(count_query)
    total_records = total_records_result.scalar_one()
    offset = (page - 1) * page_size
    query = select(model).where(*filters).offset(offset).limit(page_size)
    result = await db.execute(query)
    items = result.scalars().all()
    total_pages = (total_records + page_size - 1) // page_size
    return items, total_records, total_pages

def app_success_paginated(
    data: Optional[Any] = None,
    msg: Optional[str]= None,
    code: int = 200,
    total_records: Optional[int] = None,
    total_pages: Optional[int] = None,
    current_page: Optional[int] = None,
    page_size: Optional[int] = None,
    lists: Optional[List[Dict]] = None,
    extra: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Standardized success response formatter.

    Supports paginated response if pagination params are provided.

    Args:
        data: Arbitrary response data for non-paginated response
        msg: Response message
        code: HTTP status code (default 200)
        total_records: Total number of records (for paginated)
        total_pages: Total pages count (for paginated)
        current_page: Current page number (for paginated)
        page_size: Page size (for paginated)
        lists: List of items (for paginated)

    Returns:
        Dict formatted response ready to return as JSON.
    """
    if msg is None:
        msg = "success"
    response = {
        "code": code,
        "msg": msg,
    }
    if all(v is not None for v in [total_records, total_pages, current_page, page_size, lists]):
        base_data = {
            "total_records": total_records,
            "total_pages": total_pages,
            "current_page": current_page,
            "page_size": page_size,
        }
        if extra:
            base_data.update(extra)  
        base_data["lists"] = lists 
        response["data"] = base_data
    else:
        response["data"] = data
    return response

def app_success(
    msg: Optional[str] = None,
    code: int = 200,
    data: Optional[Any] = None,
):
    """
    Standardized success response formatter.

    Args:
        msg: Success message
        code: HTTP status code (default 200)
        data: Optional returned data

    Returns:
        Dict formatted success response
    """
    if msg is None:
        msg = "success"
    return {
        "code": code,
        "msg": msg,
        "data": data
    }

def app_error(
    msg: Optional[str] = None,
    code: int = 400,
    data: Optional[Any] = None,
):
    """
    Standardized error response formatter.

    Args:
        msg: Error message
        code: HTTP status code (default 400)
        data: Optional returned data

    Returns:
        Dict formatted error response
    """
    if msg is None:
        msg = "fail"
    return {
        "code": code,
        "msg": msg,
        "data": data
    }

def app_server_error(
    msg: Optional[str] = None,
    code: int = 500,
    data: Optional[Any] = None,
):
    """
    Standardized server error response formatter.

    Args:
        msg: Error message
        code: HTTP status code (default 500)
        data: Optional returned data

    Returns:
        Dict formatted error response
    """
    if msg is None:
        msg ="server_error"
    return {
        "code": code,
        "msg": msg,
        "data": data
    }

def hash_password(
        plain_password: str
) -> str:
    """
    Hash a plaintext password using bcrypt.
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(
    plain_password: str, 
    hashed_password: str
) -> bool:
    """
    Verify a plaintext password against a hashed password.    
    """
    return bcrypt.checkpw(
        plain_password.encode('utf-8'), 
        hashed_password.encode('utf-8')
    )

class ApproveStatus(str,Enum):
    pending = "pending"
    approved = "approved"

class Status(str,Enum):
    """
    Status has approved, pending, rejected
    """
    approved = "approved"   
    pending = "pending"
    rejected = "rejected"

def get_phnom_penh_time():
    """
    get date time in phnom penh 
    """
    phnom_penh_tz = pytz.timezone('Asia/Phnom_Penh')
    dt = datetime.now(phnom_penh_tz)
    return dt.replace(tzinfo=None)

def get_phnom_penh_time_formatted(dt: datetime) -> str:
    """
    Format a datetime object to 'Month Day Year : minute hour' 
    """
    return dt.strftime("%B %d %Y")  

class ActiveStatus(str, Enum):
    """
    Active status has active , inactive
    """
    active = "active"
    inactive = "inactive"
    
def create_access_token(
    data:dict,
    expires_delta: Optional[timedelta] = None
):
    """ 
    Create a JWT access token
    data: dick-> payload(user infor like id, username)
    expires_delta: optional custom expireation timedelta

    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
    to_encode.update({"exp": expire}) # add expiration
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(
    data:dict,
    expire_delta: Optional[timedelta] = None
):
    """
    create a jwt refresh token
    usually longer expiration than access token
    
    """

    to_encode = data.copy()
    if expire_delta:
        expire = datetime.utcnow() + expire_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRES_MINUTES)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encode_jwt

def verify_token(
    token:str = Depends(oauth2_schema)
):
    try:
        payload =jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username: str = payload.get("username")
        role: str = payload.get("role")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return {
            "username": username,
            "role": Role(role)
        }
    except JWTError:
         raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

def require_admin(
    current_user:dict = Depends(verify_token)
):
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can perform this action"
        )
    return current_user




class AppException(HTTPException):
    def __init__(self, code: int, msg: str, status_code: int = 400):
        super().__init__(status_code=status_code, detail={
            "code": code,
            "msg": msg,
            "data": None
        })

async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail
    )
    
def set_ordering(model):
    """
    Auto-assign ordering = id after insert
    """
    @event.listens_for(model, 'after_insert')
    def assign_ordering(mapper, connection, target):
        connection.execute(
            model.__table__.update()
            .where(model.id == target.id)
            .values(ordering=target.id)
        )

class QuestionType(str, Enum):
    single_choice = "single_choice"   # One correct answer (Radio buttons)
    multiple_choice = "multiple_choice" # Multiple correct answers (Checkboxes)
    true_false = "true_false"
    short_answer = "short_answer"    # Text input
    matching = "matching"