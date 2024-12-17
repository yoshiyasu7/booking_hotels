from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select

from app.main import lifespan #?
from app.models import BookingORM, HotelORM #?,
from app.schemas import BookingResponse, BookingCreate

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],
)

@router.post("/", response_model=BookingResponse)
async def create_booking(booking_data: BookingCreate, db: Depends(lifespan)):
    result = await db.execute(select(HotelORM).filter_by(id=booking_data.hotel_id))
    hotel = result.scalar_one_or_none()
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")
    if hotel.rooms_available < booking_data.rooms_booked:
        raise HTTPException(status_code=400, detail="Not enough rooms available")

    booking = BookingORM(**booking_data.model_dump())
    hotel.rooms_available -= booking.rooms_booked

    db.add(booking)
    await db.commit()
    await db.refresh(booking)
    return booking


@router.get("/", response_model=List[BookingResponse])
async def read_bookings(db: Depends(lifespan)):
    result = await db.execute(select(BookingORM))
    return result.scalars().all()
