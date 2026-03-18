from sqlalchemy import TIMESTAMP, Column, Integer, String, Float, Date, Time, DateTime,Text, CHAR, Index, Enum as SqlEnum,ARRAY
from sqlalchemy.orm import relationship
from typing import Literal
from app.base.database import Base
from datetime import datetime,timezone
from sqlalchemy import Enum as SqlEnum  
import uuid
from sqlalchemy.dialects.postgresql import UUID
from app.base.untility import set_ordering,get_phnom_penh_time,get_phnom_penh_time_formatted

class Category(Base):
    __tablename__ = "category"

    id = Column(Integer,primary_key=True,index=True)
    name = Column(String(255),unique=True)
    description = Column(Text,nullable=True)
    created_at = Column(DateTime,default=get_phnom_penh_time)
    updated_at = Column(DateTime,default=get_phnom_penh_time)
    ordering = Column(Integer,default=0)

set_ordering(Category)

