from fastapi import APIRouter

from app.database import SessionDependency
from app.repository.users import UsersRepository
from app.schemas import UserCreate, UserId

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("/")
async def create_user(user_data: UserCreate, session: SessionDependency) -> UserId:
    user_id = await UsersRepository.create_user(user_data, session)
    return {"ok": True, "user_id": user_id}
