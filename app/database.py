from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

# создание асинхронного движка
async_engine = create_async_engine(
    "sqlite+aiosqlite://hotels.db",
    echo=True # вывод SQL-запросов для отладки
)
# создание асинхронной сессии
new_session = async_sessionmaker(async_engine,
                                 connect_args={"check_same_thread": False}, # нужен для многопоточных соединений к SQLite
                                 expire_on_commit=False,
                                 class_=AsyncSession)

# используем DeclarativeBase для создания базового класса
class Base(DeclarativeBase):
    pass
