from pydantic import BaseModel, EmailStr


class UserId(BaseModel):
    ok: bool = True
    user_id: int


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr


class HotelCreate(BaseModel):
    hotel_name: str
    hotel_location: str
    owner_id: int
    price_per_night: float
    rooms_available: int


class HotelResponse(BaseModel):
    id: int
    hotel_name: str
    hotel_location: str
    owner_id: int
    price_per_night: float
    rooms_available: int


class HotelId(BaseModel):
    ok: bool = True
    hotel_id: int


class BookingCreate(BaseModel):
    hotel_id: int
    user_id: int
    guest_name: str
    rooms_booked: int


class BookingResponse(BaseModel):
    id: int
    guest_name: str


class BookingId(BaseModel):
    ok: bool = True
    booking_id: int


class MessageResponse(BaseModel):
    message: str
