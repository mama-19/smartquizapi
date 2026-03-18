from sqlalchemy import TIMESTAMP, Column, Integer,TEXT, String, Float, Date, Time, DateTime,Text, CHAR, Index, Enum as SqlEnum,ARRAY
from sqlalchemy.orm import relationship
from typing import Literal
from app.base.database import Base
from datetime import datetime,timezone
from sqlalchemy import Enum as SqlEnum  
import uuid
from sqlalchemy.dialects.postgresql import UUID
from app.base.untility import set_ordering,QuestionType,get_date_time_formatted,ActiveStatus,get_phnom_penh_time,get_phnom_penh_time_formatted

class Question(Base):
    __tablename__ ="question"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    quiz_id = Column(Integer, primary_key=True,index=True)
    content = Column(TEXT,nullable=True)
    question_type = Column(SqlEnum(QuestionType,name="question_type_enum"),nullable=True,default=QuestionType.multiple_choice)
    is_active = Column(SqlEnum(ActiveStatus, name="active_enum"), nullable=True,default=ActiveStatus.active)
    point = Column(Integer,nullable=Text,default=0)
    created_at = Column(DateTime,default=get_phnom_penh_time)
    updated_at = Column(DateTime,default=get_phnom_penh_time,onupdate=get_phnom_penh_time)
    ordering = Column(Integer, default=0)

    # answers = relationship("Answer", back_populates="question")

set_ordering(Question)