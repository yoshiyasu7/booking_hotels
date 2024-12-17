from pydantic import BaseModel


class HotelCreate(BaseModel):
    name: str
    location: str
    price_per_night: float
    rooms_available: int


class HotelResponse(BaseModel):
    id: int
    name: str
    location: str
    price_per_night: float
    rooms_available: int

    class Config:
        orm_mode = True


class BookingCreate(BaseModel):
    hotel_id: int
    guest_name: str
    rooms_booked: int

class BookingResponse(BaseModel):
    id: int
    guest_name: str

    class Config:
        orm_mode = True


class MessageResponse(BaseModel):
    message: str
