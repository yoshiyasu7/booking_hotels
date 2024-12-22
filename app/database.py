from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

# создание асинхронного движка
async_engine = create_async_engine(
    "sqlite+aiosqlite:///hotels.db",
    echo=True # вывод SQL-запросов для отладки
)
# создание асинхронной сессии
new_session = async_sessionmaker(async_engine, expire_on_commit=False)

# используем DeclarativeBase для создания базового класса
class Base(DeclarativeBase):
    pass
