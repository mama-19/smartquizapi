from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.base.database import get_db
from app.base.untility import require_admin
from app.schemas.category.category_schema import CategoryData
from app.schemas.quiz.quiz_schema import QuizData
from app.schemas.question.question_schema import QuestionData
from app.schemas.answer.answer_schema import AnswerData

from app.controller.api.backend.Category.category_controller import (
    create_category, update_category, delete_category
)
from app.controller.api.backend.quiz.quiz_controller import (
    create_quiz, update_quiz, delete_quiz
)
from app.controller.api.backend.question.question_controller import (
    create_question, update_question, delete_question
)
from app.controller.api.backend.answer.answer_controller import (
    create_answer, update_answer, delete_answer
)

admin_router = APIRouter(
    prefix="/smartquizs",
    dependencies=[Depends(require_admin)],
    tags=["Admin"]
)

# Category
@admin_router.post("/category/create")
async def create_category_route(
    db: AsyncSession = Depends(get_db),
    category: CategoryData = Depends(CategoryData.as_form)
):
    return await create_category(db, category)

@admin_router.put("/category/update")
async def update_category_route(
    db: AsyncSession = Depends(get_db),
    category_id: Optional[int] = Query(None),
    category: CategoryData = Depends(CategoryData.as_form)
):
    return await update_category(db, category_id, category)

@admin_router.delete("/category/delete")
async def delete_category_route(
    db: AsyncSession = Depends(get_db),
    category_id: Optional[int] = Query(None)
):
    return await delete_category(db, category_id)

# Quiz
@admin_router.post("/quizs/create")
async def create_quiz_route(
    db: AsyncSession = Depends(get_db),
    quiz: QuizData = Depends(QuizData.as_form)
):
    return await create_quiz(db, quiz)

@admin_router.put("/quizs/update")
async def update_quiz_route(
    db: AsyncSession = Depends(get_db),
    quiz_id: Optional[int] = Query(None),
    quiz: QuizData = Depends(QuizData.as_form)
):
    return await update_quiz(db, quiz_id, quiz)

@admin_router.delete("/quizs/delete")
async def delete_quiz_route(
    db: AsyncSession = Depends(get_db),
    quiz_id: Optional[int] = Query(None)
):
    return await delete_quiz(db, quiz_id)

# Question routes
@admin_router.post("/question/create")
async def admin_create_question(db: AsyncSession = Depends(get_db), question: QuestionData = Depends(QuestionData.as_form)):
    return await create_question(db, question)

@admin_router.put("/question/update")
async def admin_update_question(db: AsyncSession = Depends(get_db), question_id: int = Query(...), question: QuestionData = Depends(QuestionData.as_form)):
    return await update_question(db, question_id=question_id, update_question=question)

@admin_router.delete("/question/delete")
async def admin_delete_question(db: AsyncSession = Depends(get_db), question_id: int = Query(...)):
    return await delete_question(db, question_id=question_id)

# Answer routes
@admin_router.post("/answer/create")
async def admin_create_answer(db: AsyncSession = Depends(get_db), answer: AnswerData = Depends(AnswerData.as_form)):
    return await create_answer(db, answer)

@admin_router.put("/answer/update")
async def admin_update_answer(db: AsyncSession = Depends(get_db), answer_id: int = Query(...), answer: AnswerData = Depends(AnswerData.as_form)):
    return await update_answer(db, answer_id=answer_id, update_answer=answer)

@admin_router.delete("/answer/delete")
async def admin_delete_answer(db: AsyncSession = Depends(get_db), answer_id: int = Query(...)):
    return await delete_answer(db, answer_id=answer_id)



