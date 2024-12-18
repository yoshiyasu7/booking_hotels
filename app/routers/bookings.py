from typing import List

from fastapi import APIRouter, Depends

from app.schemas import BookingResponse, BookingCreate, MessageResponse


router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],
)

@router.post("/", response_model=BookingResponse)
async def create_booking(hotel_data: BookingCreate, db: Depends()):
    pass

@router.get("/", response_model=List[BookingResponse])
async def read_bookings(db: Depends()):
    pass

@router.delete("/{booking_id}", response_model=MessageResponse)
async def cancel_bookings(db: Depends()):
    pass