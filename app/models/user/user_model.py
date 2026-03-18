from sqlalchemy import TIMESTAMP, Column, Integer, String,Boolean, Float, Date, Time, DateTime,Text, CHAR, Index, Enum as SqlEnum,ARRAY
from sqlalchemy.orm import relationship
from typing import Literal
from app.base.database import Base
from datetime import datetime,timezone
from sqlalchemy import Enum as SqlEnum 
from app.base.untility import ActiveStatus,Role,set_ordering,get_phnom_penh_time
import uuid
from sqlalchemy.dialects.postgresql import UUID
# use
class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False,unique=True)
    email = Column(String(191), nullable=False, unique=True, index=True)
    password = Column(String(255), nullable=False)
    is_active = Column(SqlEnum(ActiveStatus, name="active_enum"), nullable=True,default=ActiveStatus.active)
    role = Column(SqlEnum(Role,name="role_enum"),nullable=True,default=Role.user)
    created_at = Column(DateTime,default=get_phnom_penh_time)
    updated_at = Column(DateTime,default=get_phnom_penh_time,onupdate=get_phnom_penh_time)
    ordering = Column(Integer, default=0)
    attempts = relationship("QuizAttempt", back_populates="user")

    # attempts = relationship("QuizAttempt", back_populates="user")

set_ordering(User)
    