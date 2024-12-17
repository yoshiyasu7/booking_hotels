from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select

from app.main import lifespan #?
from app.models import HotelORM
from app.schemas import HotelResponse, HotelCreate

router = APIRouter(
    prefix="/hotels",
    tags=["Hotels"],
)

@router.post("/", response_model=HotelResponse)
async def create_hotel(hotel_data: HotelCreate, db: Depends(lifespan)):
    hotel = HotelORM(**hotel_data.model_dump())
    db.add(hotel)
    await db.commit()
    await db.refresh(hotel)
    return hotel

@router.get("/", response_model=List[HotelResponse])
async def read_hotels(db: Depends(lifespan)):
    result = await db.execute(select(HotelORM))
    return result.scalars().all()