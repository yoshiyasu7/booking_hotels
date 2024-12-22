from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base

# создаём модель таблицы hotels базы данных
class HotelORM(Base):
    __tablename__ = "hotels"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    location: Mapped[str]
    price_per_night: Mapped[float]
    rooms_available: Mapped[int]

    bookings: Mapped[List["BookingORM"]] = relationship(back_populates="hotel")

# создаём модель таблицы bookings базы данных
class BookingORM(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    guest_name: Mapped[str]
    rooms_booked: Mapped[int]

    hotel: Mapped[HotelORM] = relationship(back_populates="bookings")

