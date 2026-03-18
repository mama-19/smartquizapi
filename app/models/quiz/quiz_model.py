from sqlalchemy import TIMESTAMP, Column, Integer, String, Float, Date, Time, DateTime,Text, CHAR, Index, Enum as SqlEnum,ARRAY
from sqlalchemy.orm import relationship
from typing import Literal
from app.base.database import Base
from datetime import datetime,timezone
from sqlalchemy import Enum as SqlEnum  
import uuid
from sqlalchemy.dialects.postgresql import UUID
from app.base.untility import set_ordering,get_date_time_formatted,ActiveStatus,get_phnom_penh_time,get_phnom_penh_time_formatted

class Quiz(Base):
    __tablename__ ="quiz"

    id = Column(Integer,primary_key=True,index=True)
    title = Column(String(255),nullable=True)
    description = Column(String(255),nullable=True)
    category_id = Column(Integer,nullable=False)
    time_limit = Column(Integer,nullable=True)
    total_question = Column(Integer,nullable=True)
    is_active = Column(SqlEnum(ActiveStatus, name="active_enum"), nullable=True,default=ActiveStatus.active)
    created_at = Column(DateTime,default=get_phnom_penh_time)
    updated_at = Column(DateTime,default=get_phnom_penh_time,onupdate=get_phnom_penh_time)
    ordering = Column(Integer, default=0)
set_ordering(Quiz)