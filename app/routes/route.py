from fastapi import APIRouter, Depends, HTTPException, Query, Form
from sqlalchemy.ext.asyncio import AsyncSession
from app.base.database import get_db
from typing import Optional, Union,List
import uuid 
from app.controller.api.backend.Category.category_controller import (
    list_category,
    create_category,
    delete_category,
    update_category
)
from app.base.untility import verify_token,require_admin
from app.schemas.category.category_schema import CategoryData
from app.schemas.user.user_schema import UserData
from app.controller.api.backend.User.user_controller import(
    create_user,
    list_user,
    update_user,
    delete_user,
    login,
    get_current_user
)
from app.controller.api.backend.quiz.quiz_controller import (
    create_quiz,
    list_quiz,
    update_quiz,
    update_quiz_active_status,
    delete_quiz
    )
from app.models.quiz.quiz_model import ActiveStatus
from app.schemas.quiz.quiz_schema import QuizData
from app.models.question.question_model import ActiveStatus,QuestionType
from app.schemas.question.question_schema import QuestionData
from app.controller.api.backend.question.question_controller import(
    list_question,
    create_question,
    update_question,
    update_question_active_status,
    delete_question
)
from app.models.answer.answer_model import ActiveStatus
from app.schemas.answer.answer_schema import AnswerData
from app.controller.api.backend.answer.answer_controller import (
    create_answer,
    list_anwser,
    update_answer,
    delete_answer,
    update_answer_active_status
)
from app.controller.api.backend.quiz_attempt.quiz_attempt_controller import(
    create_quiz_attempt,
    list_quiz_attempt
)
from app.schemas.quiz_attempt.quiz_attempt_schema import QuizAttemptData
from app.controller.api.backend.quiz_attempt_answer.quiz_attemp_answer_controller import(
    create_quiz_attempt_answer,
    list_quiz_attempt_answer
)
from app.schemas.quiz_attempt_answer.quiz_attempt_answer_schema import QuizAttemptAnswerData
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/smartquizs/auth/login")
from app.models.user.user_model import ActiveStatus,Role
router = APIRouter()
# router = APIRouter(
   
# )

""" Category route """
@router.get("/tes")
def func_test():
    return {"Hello": "World"}
@router.get("/smartquizs/category/lists")
async def func_list_category(
    db:AsyncSession = Depends(get_db),
    curren_user = Depends(verify_token),
    name:Optional[str] = None,
    page:int = 1,
    page_size: int = 10,
):
    return await list_category(
        db=db,
        name=name,
        page=page,
        page_size=page_size
    )
@router.post("/smartquizs/category/create")
async def func_create_category(
    db:AsyncSession = Depends(get_db),
    curren_user = Depends(require_admin),
    category: CategoryData = Depends(CategoryData.as_form)
):
    return await create_category(db=db,category=category)

@router.put("/smartquizs/category/update")
async def func_update_category(
    db:AsyncSession = Depends(get_db),
    curren_user = Depends(require_admin),
    category_id: Optional[int] = Query(None),
    category: CategoryData = Depends(CategoryData.as_form)
):
    return await update_category(db=db,category_id=category_id,update_category=category)

@router.delete("/smartquizs/category/delete")
async def func_delete_category(
    db:AsyncSession = Depends(get_db),
    curren_user = Depends(require_admin),
    category_id:Optional[int] = Query(None)
):
    return await delete_category(db=db,category_id=category_id)

""" User Route """
@router.post("/smartquizs/auth/register")
async def func_create_user(
    db:AsyncSession = Depends(get_db),
    user: UserData = Depends(UserData.as_form)
):
    return await create_user(db=db,user=user)
@router.get("/smartquizs/users/lists")
async def func_list_user(
    db:AsyncSession = Depends(get_db),
    name:Optional[str] = Query(None),
    role:Optional[Role] = Query(None),
    curren_user = Depends(verify_token),
    is_active:Optional[ActiveStatus] = Query(None),
    page:int = 1,
    page_size: int = 10
):
    return await list_user(
        db=db,
        name=name,
        role=role,
        is_active=is_active,
        page=page,
        page_size=page_size
    )
@router.put("/smartquizs/users/update")
async def func_update_user(
    db:AsyncSession = Depends(get_db),
    user: UserData = Depends(UserData.as_form),
    curren_user = Depends(verify_token),
    user_id: Optional[int] = Query(None)
):
    return await update_user(db=db,user_id=user_id,update_user=user)
@router.delete("/smartquizs/users/delete")
async def func_delete_user(
    db:AsyncSession = Depends(get_db),
    curren_user = Depends(require_admin),
    user_id: Optional[int] = Query(...)
):
    return await delete_user(db=db,user_id=user_id)
@router.post("/smartquizs/auth/login")
async def func_login(
    db:AsyncSession = Depends(get_db),
    user_form : OAuth2PasswordRequestForm = Depends(),
):
    return await login(db=db,user_form=user_form)

@router.get("/smartquizs/auth/get-me")
async def func_get_me(
    db:AsyncSession = Depends(get_db),
    curren_user = Depends(verify_token),
    username:str = Depends(verify_token)
):
    return await get_current_user(username=username,db=db)

""" Quiz route """
@router.get("/smartquizs/quizs/lists")
async def func_list_quiz(
    db:AsyncSession = Depends(get_db),
    title:Optional[str] = Query(None),
    page:int = 1,
    page_size:int = 10,
    curren_user = Depends(verify_token),
):
    return await list_quiz(
        db=db,
        title=title,
        page=page,
        page_size=page_size,
    )
@router.post("/smartquizs/quizs/create")
async def func_create_quiz(
    db:AsyncSession = Depends(get_db),
    quiz:QuizData = Depends(QuizData.as_form),
    curren_user = Depends(require_admin),
):
    return await create_quiz(db=db,quiz=quiz)
@router.put("/smartquizs/quizs/update")
async def func_update_quiz(
    db:AsyncSession = Depends(get_db),
    quiz_id:Optional[int] =Query(None),
    quiz: QuizData = Depends(QuizData.as_form),
    curren_user = Depends(require_admin),
):
    return await update_quiz(
        db=db,
        quiz_id=quiz_id,
        update_quiz=quiz
    )
@router.put("/smartquizs/quizs/update-active-status")
async def func_update_active_status(
    db:AsyncSession = Depends(get_db),
    quiz_id:Optional[int] = Query(None),
    active_status:Optional[ActiveStatus] = Form(None),
    curren_user = Depends(verify_token),
):
    return await update_quiz_active_status(
        db=db,
        quiz_id=quiz_id,
        active_status=active_status
    )
@router.delete("/smartquizs/quizs/delete")
async def func_delete_quiz(
    db:AsyncSession = Depends(get_db),
    quiz_id:Optional[int] = Query(None),
    curren_user = Depends(verify_token),
):
    return await delete_quiz(
        db=db,
        quiz_id=quiz_id
    )

""" Question Router """
@router.get("/smartquizs/question/lists")
async def func_list_question(
    db:AsyncSession = Depends(get_db),
    curren_user = Depends(verify_token),
    page:int =1,
    page_size:int = 10,
):
    return await list_question(db=db,page=page,page_size=page_size)

@router.post("/smartquizs/question/create")
async def func_create_question(
    db:AsyncSession = Depends(get_db),
    question:QuestionData = Depends(QuestionData.as_form),
    curren_user = Depends(verify_token),
):
    return await create_question(db=db,question=question)
@router.put("/smartquizs/question/update")
async def func_update_question(
    db:AsyncSession = Depends(get_db),
    question:QuestionData = Depends(QuestionData.as_form),
    question_id:Optional[int] = Query(None),
    curren_user = Depends(verify_token),
):
    return await update_question(
        db=db,
        update_question=question,
        question_id=question_id
    )
@router.put("/smartquizs/question/update-active-status")
async def func_update_active_status_question(
    db:AsyncSession = Depends(get_db),
    active_status:Optional[ActiveStatus] = Form(None),
    question_id:Optional[int] = Query(None),
    curren_user = Depends(verify_token),
):
    return await update_question_active_status(
        db=db,
        active_status=active_status,
        question_id=question_id
    )
@router.delete("/smartquizs/question/delete")
async def func_delete_question(
    db:AsyncSession = Depends(get_db),
    question_id:Optional[int] = Query(None),
    curren_user = Depends(verify_token),
):
    return await delete_question(
        db=db,
        question_id=question_id
    )

"Answer route"

@router.get("/smartquizs/answers/lists")
async def func_list_answer(
    db:AsyncSession = Depends(get_db),
    page:int = 1,
    page_size: int = 10,
    curren_user = Depends(verify_token),
):
    return await list_anwser(
        db=db,
        page=page,
        page_size=page_size
    )
@router.post("/smartquizs/answers/create")
async def func_create_answer(
    db:AsyncSession = Depends(get_db),
    answer:AnswerData = Depends(AnswerData.as_form),
    curren_user = Depends(verify_token),
):
    return await create_answer(
        db=db,
        answer=answer
    )
@router.put("/smartquizs/answers/update")
async def func_update_answer(
    db:AsyncSession = Depends(get_db),
    answer:AnswerData = Depends(AnswerData.as_form),
    answer_id:Optional[int] = Query(None),
    curren_user = Depends(verify_token),
):
    return await update_answer(
        db=db,
        answer_id=answer_id,
        update_answer=answer
    )
@router.delete("/smartquizs/answers/delete")
async def func_delete_answer(
    db:AsyncSession = Depends(get_db),
    answer_id:Optional[int] = Query(None),
    curren_user = Depends(verify_token),
):
    return await delete_answer(
        db=db,
        answer_id=answer_id
    )

"""  Quiz Attempt Route"""
@router.post("/smartquizs/quiz_attempt/create")
async def func_create_quiz_attempt(
    db:AsyncSession = Depends(get_db),
    attempt:QuizAttemptData = Depends(QuizAttemptData.as_form),
    curren_user = Depends(verify_token),

):
    return await create_quiz_attempt(db=db,attempt=attempt)
@router.get("/smartquizs/quiz_attempt/lists")
async def func_list_quiz_attempt(
    db: AsyncSession = Depends(get_db),
    user_id: Optional[int] = Query(None),
    quiz_id: Optional[int] = Query(None),
    page: int = 1,
    page_size: int = 10,
    curren_user = Depends(verify_token),

):
    return await list_quiz_attempt(
        db=db,
        user_id=user_id,
        quiz_id=quiz_id,
        page=page,
        page_size=page_size
    )

""" quiz attempt answer """

@router.post("/smartquizs/quiz_attempt_answer/create")
async def func_create_quiz_attempt_answer(
    db:AsyncSession = Depends(get_db),
    answer:QuizAttemptAnswerData = Depends(QuizAttemptAnswerData.as_form),
    curren_user = Depends(verify_token),

):
    return await create_quiz_attempt_answer(
        db=db,
        answer=answer
    )
@router.get("/smartquizs/quiz_attempt_answer/lists")
async def func_list_quiz_attempt_answer(
    db:AsyncSession = Depends(get_db),
    quiz_attempt_id:Optional[int] = Query(None),
    curren_user = Depends(verify_token),
):
    return await list_quiz_attempt_answer(
        db=db,
        quiz_attempt_id=quiz_attempt_id
    )


