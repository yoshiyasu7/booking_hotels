from fastapi import HTTPException
from sqlalchemy import select

from app.database import SessionDependency
from app.models import UserORM
from app.schemas import UserCreate, UserResponse, UserId, UserUpdate, UserDelete
from app.security.encryption import encrypt_data, decrypt_data
from app.security.password import hash_password


class UsersRepository:
    @classmethod
    async def create_user(cls, user_data: UserCreate, session: SessionDependency) -> UserId:
        data = user_data.model_dump()
        data["password"] = hash_password(user_data.password)
        data["email"] = encrypt_data(user_data.email)

        new_user = UserORM(**data)
        session.add(new_user)
        await session.flush()
        await session.commit()
        return {"ok": True, "user_id": new_user.id}

    @classmethod
    async def get_user_by_email(cls, user_email: str, session: SessionDependency) -> UserResponse:
        encrypted_email = encrypt_data(user_email)
        query = select(UserORM).where(UserORM.email == encrypted_email)
        result = await session.execute(query)
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user.email = decrypt_data(user_email)
        return user.model_dump(exclude=["password"])

    @classmethod
    async def update_user(cls, update_data: UserCreate, session: SessionDependency) -> UserUpdate:
        user = await UsersRepository.get_user_by_email(update_data.email, session)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if update_data.password:
            update_data.password = hash_password(update_data.password)

        if update_data.email:
            update_data.email = encrypt_data(update_data.email)

        for key, value in update_data.model_dump().items():
            setattr(user, key, value)

        await session.flush()
        await session.commit()
        return {"message": "User updated successfully", "username": user.username, "email": user.email}

    @classmethod
    async def delete_user(cls, user_email: str, session: SessionDependency) -> UserDelete:
        user = await UsersRepository.get_user_by_email(user_email, session)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        await session.delete(user)
        await session.commit()
        return {"message": "User deleted successfully"}
