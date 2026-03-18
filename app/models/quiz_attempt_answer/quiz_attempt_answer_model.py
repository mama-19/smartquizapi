from sqlalchemy import TIMESTAMP, Column,Boolean,ForeignKey,func, Integer,TEXT, String, Float, Date, Time, DateTime,Text, CHAR, Index, Enum as SqlEnum,ARRAY
from sqlalchemy.orm import relationship
from typing import Literal
from app.base.database import Base
from datetime import datetime,timezone
from sqlalchemy import Enum as SqlEnum  
import uuid
from sqlalchemy.dialects.postgresql import UUID
from app.base.untility import set_ordering,QuestionType,get_date_time_formatted,ActiveStatus,get_phnom_penh_time,get_phnom_penh_time_formatted

class QuizAttemptAnswer(Base):
    __tablename__ = "quiz_attempt_answer"

    # id = Column(Integer, primary_key=True, index=True)
    # quiz_attempt_id = Column(Integer, ForeignKey("quiz_attempt.id", ondelete="CASCADE"))
    # question_id = Column(Integer, ForeignKey("question.id"))
    # answer_id = Column(Integer, ForeignKey("answer.id"))
    # is_correct = Column(Boolean)
    # answered_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    # quiz_attempt = relationship("QuizAttempt", back_populates="answers")
    # question = relationship("Question")
    # answer = relationship("Answer")


    id = Column(Integer, primary_key=True)
    quiz_attempt_id = Column(Integer, ForeignKey("quiz_attempt.id"))
    question_id = Column(Integer)
    answer_id = Column(Integer)
    is_correct = Column(Boolean)
    answered_at = Column(DateTime,default=get_phnom_penh_time)

    quiz_attempt = relationship("QuizAttempt", back_populates="answers")