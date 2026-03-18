from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from app.base.database import get_db
from app.controller.api.backend.User.user_controller import create_user, login, get_current_user
from app.schemas.user.user_schema import UserData
from app.base.untility import verify_token

auth_route = APIRouter(prefix="/auth", tags=["Auth"])

@auth_route.post("/register")
async def register(
    db: AsyncSession = Depends(get_db),
    user: UserData = Depends(UserData.as_form)
):
    return await create_user(db, user)

@auth_route.post("/login")
async def login_user(
    db: AsyncSession = Depends(get_db),
    form: OAuth2PasswordRequestForm = Depends()
):
    return await login(db, form)

@auth_route.get("/me")
async def get_me(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(verify_token)
):
    return await get_current_user(db, current_user)
