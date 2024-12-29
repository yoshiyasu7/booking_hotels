from typing import Annotated, List

from fastapi import APIRouter, Depends

from app.repository.users import UsersRepository
from app.schemas import UserCreate, UserId

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("/")
async def create_user(user_data: Annotated[UserCreate, Depends()]) -> UserId:
    user_id = await UsersRepository.create_user(user_data)
    return {"ok": True, "user_id": user_id}
