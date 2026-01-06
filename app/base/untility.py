# app/base/common.py
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
from datetime import datetime, time
from fastapi import Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy import event
from fastapi.responses import StreamingResponse
from io import BytesIO
from app.base.translate import get_translation, set_lang

T = TypeVar("T")

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
        msg = get_translation("success")
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
        msg = get_translation("success")
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
        msg = get_translation("fail")
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
        msg = get_translation("server_error")
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

class GenderEnum(str, Enum):
    """
    get gender Male,  Female
    """
    Male = "Male"
    Female = "Female"

class IsResignEnum(str, Enum):
    """
    Resign have Yes, No
    """
    No = "No"   # active
    Yes = "Yes" # resigned
    
async def verify_token(
    token: str = Query(...),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        text("SELECT * FROM hr_employee WHERE app_token = :token"),
        {"token": token.strip()}
    )
    employee = result.fetchone()
    if employee is None:
        raise AppException(code=400, msg=get_translation("invalid_token"))
    return employee

async def tenant_verify_token(
    token: str = Query(...),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        text("SELECT * FROM tenant_admin WHERE app_token = :token"),
        {"token": token.strip()}
    )
    employee = result.fetchone()
    if employee is None:
        raise AppException(code=400, msg=get_translation("invalid_token"))
    return employee

async def check_existing_record(
    db: AsyncSession,
    table_name: str,
    id_value: Optional[int],
    translate:str
):
    """
    Check if a record with the given ID exists and is active.
    Returns:
        None if valid, else app_error.
    """
    if id_value is not None:
        query = f"""
            SELECT 1 FROM {table_name}
            WHERE id = :id AND is_active = :active
        """
        params = {"id": id_value, "active": "active"}
        result = await db.execute(text(query), params)
        exists = result.scalar_one_or_none()
        if exists is None:
            return app_error(msg=get_translation(translate))
    return None

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

def export_file_response(file: BytesIO, filename: str, media_type: str) -> StreamingResponse:
    """
    Custom export response for Excel or PDF files.

    :param file: BytesIO file content
    :param filename: Name of the file (e.g., 'report.pdf', 'data.xlsx')
    :param media_type: MIME type (e.g., 'application/pdf', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    :return: StreamingResponse for download
    """
    file.seek(0) 
    return StreamingResponse(
        content=file,
        media_type=media_type,
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"'
        }
    )

EXCLUDED_PATHS = [
    "/auths/login"
] 
async def protect_route(
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """
    Route protection to check user permissions.
    """
    current_path = request.url.path
    if current_path in EXCLUDED_PATHS:
        return 
    token = request.query_params.get("token")
    if not token:
        raise AppException(code=400, msg=get_translation("app_token_required"))
    employee = await verify_token(token=token, db=db)
    user_id = employee.id
    admin_check = await db.execute(text("""
        SELECT 1
        FROM permission_group_access pga
        JOIN permission_group pg ON pga.group_id = pg.id
        WHERE pga.uid = :uid AND pg.rules LIKE '%*%' AND pg.is_active = 'active' 
    """), {"uid": user_id})
    if admin_check.scalar() is not None:
        return employee
    result = await db.execute(text("""
        SELECT r.route
        FROM permission_group_access pga
        JOIN permission_group pg ON pga.group_id = pg.id 
        JOIN LATERAL unnest(string_to_array(pg.rules, ',')) AS rule_ids(rule_id_text) ON TRUE
        JOIN permission_rule r ON r.id = rule_ids.rule_id_text::int
        WHERE pga.uid = :uid AND rule_ids.rule_id_text ~ '^[0-9]+$' and pg.is_active = 'active' and r.is_active = 'active'
    """), {"uid": user_id})
    allowed_routes = [row[0] for row in result.fetchall()]
    if current_path not in allowed_routes:
        raise AppException(code=403, msg=get_translation("unautherized_access"))
    return  employee

EXCLUDED_PATHS_TENANT = [
    "/auths/login",
    "/auths/permission/index",
    "/tenants/plan/index"

] 
async def tenant_protect_route(
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """
    Route protection to check user permissions.
    """
    current_path = request.url.path
    if current_path in EXCLUDED_PATHS_TENANT:
        return 
    token = request.query_params.get("token")
    if not token:
        raise AppException(code=400, msg=get_translation("app_token_required"))
    employee = await tenant_verify_token(token=token, db=db)
    user_id = employee.id
    admin_check = await db.execute(text("""
        SELECT 1
        FROM tenant_permission_group_access pga
        JOIN tenant_permission_group pg ON pga.group_id = pg.id
        WHERE pga.uid = :uid AND pg.rules LIKE '%*%' AND pg.is_active = 'active' 
    """), {"uid": user_id})
    if admin_check.scalar() is not None:
        return employee
    result = await db.execute(text("""
        SELECT r.route
        FROM tenant_permission_group_access pga
        JOIN tenant_permission_group pg ON pga.group_id = pg.id 
        JOIN LATERAL unnest(string_to_array(pg.rules, ',')) AS rule_ids(rule_id_text) ON TRUE
        JOIN tenant_permission_rule r ON r.id = rule_ids.rule_id_text::int
        WHERE pga.uid = :uid AND rule_ids.rule_id_text ~ '^[0-9]+$' and pg.is_active = 'active' and r.is_active = 'active'
    """), {"uid": user_id})
    allowed_routes = [row[0] for row in result.fetchall()]
    if current_path not in allowed_routes:
        raise AppException(code=403, msg=get_translation("unautherized_access"))
    return  employee

async def get_language(
    lang: Optional[int] = None
):
    """"
    Set the language index based on the query parameter.
    Args:
        lang: Language index (0 for English, 1 for Khmer, 2 for Chinese)
    """
    if lang is None:
        return
    index = lang 
    if index not in [0, 1, 2]:
        index = 0
    set_lang(index)     
    from fastapi import Request, Depends
    
def generate_uuid() -> uuid.UUID:
    return uuid.uuid4()

def to_utc_naive(dt: datetime) -> datetime:
    phnom_penh_tz = pytz.timezone('Asia/Phnom_Penh')

    if dt.tzinfo is None:
        dt = phnom_penh_tz.localize(dt)
    return dt.astimezone(pytz.UTC).replace(tzinfo=None)

def end_of_day(dt: datetime) -> datetime:
    return datetime.combine(dt.date(), time.max)

def start_of_day(dt: datetime) -> datetime:
    return datetime.combine(dt.date(), time.min)

def get_date_time_formatted(dt: datetime) -> str:
    """
    Format a datetime object to 'Month Day Year : minute hour' 
    """
    return dt.strftime("%d %b %Y %I:%M %p")
