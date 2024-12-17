import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.routers import bookings, hotels

from .database import async_engine, Base, new_session


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Создание таблиц при запуске приложения
    async with async_engine.begin as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield # new_session?
    # Закрытие движка базы данных при остановке
    await async_engine.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(hotels.router)