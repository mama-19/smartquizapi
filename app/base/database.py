import os
import asyncpg
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import exc
import asyncio
from app.base.config import settings


async def wait_for_db():
    retries = 5
    while retries > 0:
        try:
            engine = create_async_engine(settings.DATABASE_URL, echo=True)
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            return engine
        except (exc.OperationalError, asyncpg.CannotConnectNowError):
            retries -= 1
            print(f"Database connection failed, retrying... ({retries} attempts left)")
            await asyncio.sleep(5)
    raise Exception("Could not connect to the database")

Base = declarative_base()
engine = None

async def get_db():
    global engine
    if engine is None:
        engine = await wait_for_db()
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session