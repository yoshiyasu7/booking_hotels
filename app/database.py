import os

from dotenv import load_dotenv, find_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

load_dotenv(find_dotenv())

# создание асинхронного движка
async_engine = create_async_engine(
    os.getenv('DATABASE_URL'),
    echo=True # вывод SQL-запросов для отладки
)
# создание асинхронной сессии
new_session = async_sessionmaker(async_engine, expire_on_commit=False)

# используем DeclarativeBase для создания базового класса
class Base(DeclarativeBase):
    pass
