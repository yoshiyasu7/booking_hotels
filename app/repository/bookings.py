from fastapi import HTTPException
from sqlalchemy import select

from app.database import new_session
from app.models import BookingORM, HotelORM
from app.schemas import BookingCreate, BookingResponse, BookingId


class BookingsRepository:
    @classmethod
    async def create_booking(cls, booking_data: BookingCreate) -> int:
        async with new_session() as session:
            query = select(HotelORM).filter_by(id=booking_data.hotel_id)
            result = await session.execute(query)
            hotel = result.scalar_one_or_none()
            if not hotel:
                raise HTTPException(status_code=404, detail="Hotel not found")
            if hotel.rooms_available < booking_data.rooms_booked:
                raise HTTPException(status_code=400, detail="Not enough rooms available")

            data = booking_data.model_dump()
            new_booking = BookingORM(**data)
            hotel.rooms_available -= new_booking.rooms_booked

            session.add(new_booking)
            await session.flush()
            await session.commit()
            return new_booking.id

    @classmethod
    async def get_bookings(cls) -> list[BookingResponse]:
        async with new_session() as session:
            query = select(BookingORM)
            result = await session.execute(query)
            booking_models = result.scalars().all()
            return booking_models

    @classmethod
    async def cancel_booking(cls, booking_id: int) -> dict:
        async with new_session() as session:
            query = select(BookingORM).filter_by(id=booking_id)
            result = await session.execute(query)
            booking = result.scalar_one_or_none()
            if not booking:
                raise HTTPException(status_code=404, detail="Booking not found")

            query = select(HotelORM).filter_by(id=booking.hotel_id)
            result = await session.execute(query)
            hotel = result.scalar_one()
            hotel.rooms_available =+ booking.rooms_booked

            await session.delete(booking)
            await session.commit()
            return {"message": "Booking cancelled successfully"}
