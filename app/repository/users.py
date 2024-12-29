from fastapi import HTTPException
from sqlalchemy import select

from app.database import SessionDependency
from app.models import UserORM
from app.schemas import UserCreate, UserResponse


class UsersRepository:
    @classmethod
    async def create_user(cls, user_data: UserCreate, session: SessionDependency) -> int:
        data = user_data.model_dump()
        new_user = UserORM(**data)
        session.add(new_user)
        await session.flush()
        await session.commit()
        return new_user.id

    @classmethod
    async def get_users(cls, session: SessionDependency) -> list[UserResponse]:
        query = select(UserORM)
        result = await session.execute(query)
        user_models = result.scalars().all()
        return user_models
