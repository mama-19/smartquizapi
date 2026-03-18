from sqlalchemy import TIMESTAMP, Column,Boolean,ForeignKey,func, Integer,TEXT, String, Float, Date, Time, DateTime,Text, CHAR, Index, Enum as SqlEnum,ARRAY
from sqlalchemy.orm import relationship
from typing import Literal
from app.base.database import Base
from datetime import datetime,timezone
from sqlalchemy import Enum as SqlEnum  
import uuid
from sqlalchemy.dialects.postgresql import UUID
from app.base.untility import set_ordering,QuestionType,get_date_time_formatted,ActiveStatus,get_phnom_penh_time,get_phnom_penh_time_formatted

class QuizAttempt(Base):
    __tablename__ = "quiz_attempt"

    # id = Column(Integer, primary_key=True, index=True)
    # # user_id = Column(Integer, ForeignKey("users.id"))
    # # quiz_id = Column(Integer, ForeignKey("quiz.id"))
    # user_id = Column(Integer,nullable=True)
    # quiz_id = Column(Integer,nullable=True)
    # score = Column(Integer, default=0)
    # started_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    # completed_at = Column(TIMESTAMP(timezone=True), nullable=True)
    # is_active = Column(SqlEnum(ActiveStatus, name="active_enum"), nullable=True,default=ActiveStatus.active)
    # created_at = Column(DateTime,default=get_phnom_penh_time)
    # updated_at = Column(DateTime,default=get_phnom_penh_time,onupdate=get_phnom_penh_time)
    # ordering = Column(Integer, default=0)
    
    # user = relationship("User", back_populates="attempts")
    # quiz = relationship("Quiz", back_populates="attempts")
    # answers = relationship("QuizAttemptAnswer", back_populates="quiz_attempt")


    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    quiz_id = Column(Integer)  # assuming quiz table exists
    score = Column(Integer, default=0)
    started_at = Column(DateTime,default=get_phnom_penh_time)
    completed_at = Column(DateTime,default=get_phnom_penh_time)

    user = relationship("User", back_populates="attempts")
    answers = relationship("QuizAttemptAnswer", back_populates="quiz_attempt")
# set_ordering(QuizAttempt)