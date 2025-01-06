from fastapi import APIRouter

from app.database import SessionDependency
from app.repository.bookings_repository import BookingsRepository
from app.schemas import BookingResponse, BookingCreate, MessageResponse, BookingId

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],
)


@router.post("/")
async def create_booking(booking_data: BookingCreate, session: SessionDependency) -> BookingId:
    booking_id = await BookingsRepository.create_booking(booking_data, session)
    return {"ok": True, "booking_id": booking_id}


@router.get("/")
async def read_bookings(session: SessionDependency) -> list[BookingResponse]:
    bookings = await BookingsRepository.get_bookings(session)
    return bookings


@router.delete("/{booking_id}")
async def delete_bookings(booking_id: int, session: SessionDependency) -> MessageResponse:
    booking_canceled = await BookingsRepository.cancel_booking(booking_id, session)
    return booking_canceled
