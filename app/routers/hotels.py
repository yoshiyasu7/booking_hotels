from fastapi import APIRouter

from app.database import SessionDependency
from app.repository.hotels import HotelsRepository
from app.schemas import HotelResponse, HotelCreate, MessageResponse, HotelId

router = APIRouter(
    prefix="/hotels",
    tags=["Hotels"],
)


@router.post("/")
async def create_hotel(hotel_data: HotelCreate, session: SessionDependency) -> HotelId:
    hotel_id = await HotelsRepository.create_hotel(hotel_data, session)
    return {"ok": True, "hotel_id": hotel_id}


@router.get("/")
async def read_hotels(session: SessionDependency) -> list[HotelResponse]:
    hotels = await HotelsRepository.get_hotels(session)
    return hotels


@router.put("/{hotel_id}")
async def update_hotels(hotel_id: int, hotel_data: HotelCreate, session: SessionDependency) -> MessageResponse:
    hotel_updated = await HotelsRepository.update_hotel(hotel_id, hotel_data, session)
    return hotel_updated


@router.delete("/{hotel_id}")
async def delete_hotels(hotel_id: int, session: SessionDependency) -> MessageResponse:
    hotel_deleted = await HotelsRepository.delete_hotel(hotel_id, session)
    return hotel_deleted
