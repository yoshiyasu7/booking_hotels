from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


# создаём модель таблицы users базы данных
class UserORM(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]

    hotels: Mapped[List["HotelORM"]] = relationship(back_populates="owner")
    bookings: Mapped[List["BookingORM"]] = relationship(back_populates="user")


# создаём модель таблицы hotels базы данных
class HotelORM(Base):
    __tablename__ = "hotels"

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_name: Mapped[str]
    hotel_location: Mapped[str]
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    price_per_night: Mapped[float]
    rooms_available: Mapped[int]

    owner: Mapped[UserORM] = relationship(back_populates="hotels")
    bookings: Mapped[List["BookingORM"]] = relationship(back_populates="hotel")


# создаём модель таблицы bookings базы данных
class BookingORM(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    guest_name: Mapped[str]
    rooms_booked: Mapped[int]

    user: Mapped[UserORM] = relationship(back_populates="bookings")
    hotel: Mapped[HotelORM] = relationship(back_populates="bookings")
