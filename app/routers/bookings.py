from typing import List, Annotated

from fastapi import APIRouter, Depends

from app.repository.bookings import BookingsRepository
from app.schemas import BookingResponse, BookingCreate, MessageResponse, BookingId

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],
)


@router.post("/")
async def create_booking(booking_data: Annotated[BookingCreate, Depends()]) -> BookingId:
    booking_id = await BookingsRepository.create_booking(booking_data)
    return {"ok": True, "booking_id": booking_id}


@router.get("/")
async def read_bookings() -> list[BookingResponse]:
    bookings = await BookingsRepository.get_bookings()
    return bookings


@router.delete("/{booking_id}")
async def delete_bookings(booking_id: int) -> MessageResponse:
    booking_canceled = await BookingsRepository.cancel_booking(booking_id)
    return booking_canceled
