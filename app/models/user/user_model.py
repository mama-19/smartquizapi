from sqlalchemy import TIMESTAMP, Column, Integer, String,Boolean, Float, Date, Time, DateTime,Text, CHAR, Index, Enum as SqlEnum,ARRAY
from sqlalchemy.orm import relationship
from typing import Literal
from app.base.database import Base
from datetime import datetime,timezone
from sqlalchemy import Enum as SqlEnum  
from app.base.ionepy.ione import set_ordering,generate_uuid,ActiveStatus
import uuid
from sqlalchemy.dialects.postgresql import UUID
# use
class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(191), nullable=False, unique=True, index=True)
    password_hash = Column(String(255), nullable=False)
    # is_active = Column(SqlEnum(ActiveStatus, name="active_enum"), nullable=True, default=ActiveStatus.inactive)
   
set_ordering(User)
    