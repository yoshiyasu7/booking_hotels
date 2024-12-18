from typing import List

from fastapi import APIRouter, Depends

from app.schemas import HotelResponse, HotelCreate, MessageResponse


router = APIRouter(
    prefix="/hotels",
    tags=["Hotels"],
)

@router.post("/", response_model=HotelResponse)
async def create_hotel(hotel_data: HotelCreate, db: Depends()):
    pass

@router.get("/", response_model=List[HotelResponse])
async def read_hotels(db: Depends()):
    pass

@router.put("/{hotel_id}", response_model=MessageResponse)
async def update_hotels(db: Depends()):
    pass

@router.delete("/{hotel_id}", response_model=MessageResponse)
async def delete_hotels(db: Depends()):
    pass