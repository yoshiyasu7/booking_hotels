from fastapi import APIRouter

from app.database import SessionDependency
from app.repository.users_repository import UsersRepository
from app.schemas import UserCreate, UserId, UserResponse, UserDelete, UserUpdate

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("/")
async def create_user(user_data: UserCreate, session: SessionDependency) -> UserId:
    user = await UsersRepository.create_user(user_data, session)
    return user

@router.get("/{user_id}")
async def get_user(user_email: str, session: SessionDependency) -> UserResponse:
    user = await UsersRepository.get_user_by_email(user_email, session)
    return user

@router.put("/{user_id}")
async def update_user(update_data: UserCreate, session: SessionDependency) -> UserUpdate:
    user = await UsersRepository.update_user(update_data, session)
    return user

@router.delete("/{user_id}")
async def delete_user(user_email: str, session: SessionDependency) -> UserDelete:
    user = await UsersRepository.delete_user(user_email, session)
    return user
