# app/main.py
from fastapi import FastAPI
from app.base.untility import AppException,app_exception_handler
from app.routes import route
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

app = FastAPI()
schedule = AsyncIOScheduler()
# original even
# @app.on_event("startup")
# async def startup():
#     pass


@app.on_event("startup")
async def startup_event():
    schedule.start()
    
@app.on_event("shutdown")
async def shutdown_event():
    schedule.shutdown()

# Register the router
app.include_router(route.router)
app.add_exception_handler(AppException, app_exception_handler)




