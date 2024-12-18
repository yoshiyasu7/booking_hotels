import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.routers.hotels import router as hotels_router
from app.routers.bookings import router as bookings_router

from .database import async_engine, Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Создание таблиц при запуске приложения
    async with async_engine.begin as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Закрытие движка базы данных при остановке
    await async_engine.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(hotels_router)
app.include_router(bookings_router)