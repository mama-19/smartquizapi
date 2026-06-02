# app/main.py
from fastapi import FastAPI
from app.base.untility import AppException,app_exception_handler
from app.routes import route
from app.routes.admin_route import admin_router
from app.routes.auth_route import auth_route
from app.routes.user_route import user_router
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

app = FastAPI()
schedule = AsyncIOScheduler()
@app.on_event("startup")
async def startup_event():
    schedule.start()
    
@app.on_event("shutdown")
async def shutdown_event():
    schedule.shutdown()

# Register the router
app.include_router(auth_route)
app.include_router(admin_router)
app.include_router(user_router)
# app.include_router(route.)
# app.include_router(route.router)
app.add_exception_handler(AppException, app_exception_handler)




