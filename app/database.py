import os
from typing import Annotated

from dotenv import load_dotenv, find_dotenv
from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

load_dotenv(find_dotenv())

# создание асинхронного движка
async_engine = create_async_engine(
    os.getenv('DATABASE_URL'),
    echo=True  # вывод SQL-запросов для отладки
)
# создание асинхронной сессии в переменную new_session
new_session = async_sessionmaker(async_engine, expire_on_commit=False)


# получение новой асинхронной сессии
async def get_session():
    async with new_session() as session:
        yield session


# зависимость для получения сессии
SessionDependency = Annotated[AsyncSession, Depends(get_session)]


# используем DeclarativeBase для создания базового класса
class Base(DeclarativeBase):
    pass
