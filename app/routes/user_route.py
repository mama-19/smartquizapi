from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.base.database import get_db
from app.base.untility import verify_token
from app.controller.api.backend.Category.category_controller import list_category
from app.controller.api.backend.quiz.quiz_controller import list_quiz
from app.controller.api.backend.question.question_controller import list_question
from app.controller.api.backend.answer.answer_controller import list_anwser
from app.controller.api.backend.quiz_attempt.quiz_attempt_controller import create_quiz_attempt, list_quiz_attempt
from app.controller.api.backend.quiz_attempt_answer.quiz_attemp_answer_controller import create_quiz_attempt_answer, list_quiz_attempt_answer
from app.schemas.quiz_attempt.quiz_attempt_schema import QuizAttemptData
from app.schemas.quiz_attempt_answer.quiz_attempt_answer_schema import QuizAttemptAnswerData


user_router = APIRouter(
    prefix="/smartquizs",
    dependencies=[Depends(verify_token)],
    tags=["User"]
)

# Category list
@user_router.get("/category/lists")
async def list_category_route(
    db: AsyncSession = Depends(get_db),
    name: Optional[str] = None,
    page: int = 1,
    page_size: int = 10,
):
    return await list_category(db, name, page, page_size)

# Quiz list
@user_router.get("/quizs/lists")
async def list_quiz_route(
    db: AsyncSession = Depends(get_db),
    title: Optional[str] = None,
    page: int = 1,
    page_size: int = 10,
):
    return await list_quiz(db, title, page, page_size)

# Question list
@user_router.get("/question/lists")
async def list_question_route(
    db: AsyncSession = Depends(get_db),
    page: int = 1,
    page_size: int = 10,
):
    return await list_question(db, page, page_size)

# Answer list
@user_router.get("/answers/lists")
async def list_answer_route(
    db: AsyncSession = Depends(get_db),
    page: int = 1,
    page_size: int = 10,
):
    return await list_anwser(db, page, page_size)
@user_router.post("/quiz_attempt/create")
async def create_attempt(
    db: AsyncSession = Depends(get_db),
    attempt: QuizAttemptData = Depends(QuizAttemptData.as_form),
    current_user = Depends(verify_token)
):
    attempt.user_id = current_user["user_id"]  # enforce ownership
    return await create_quiz_attempt(db, attempt)

@user_router.get("/quiz_attempt/my-attempts")
async def my_attempts(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(verify_token),
    page: int = 1,
    page_size: int = 10
):
    return await list_quiz_attempt(db, user_id=current_user["user_id"], page=page, page_size=page_size)

# Quiz Attempt Answer
@user_router.post("/quiz_attempt_answer/create")
async def create_attempt_answer(
    db: AsyncSession = Depends(get_db),
    answer: QuizAttemptAnswerData = Depends(QuizAttemptAnswerData.as_form),
    current_user = Depends(verify_token)
):
    return await create_quiz_attempt_answer(db, answer)

@user_router.get("/quiz_attempt_answer/my-answers")
async def my_attempt_answers(
    db: AsyncSession = Depends(get_db),
    quiz_attempt_id: Optional[int] = None,
    current_user = Depends(verify_token)
):
    # optional: verify quiz_attempt_id belongs to current_user
    return await list_quiz_attempt_answer(db, quiz_attempt_id=quiz_attempt_id)