from typing import List, Annotated

from fastapi import APIRouter, Depends

from app.repository.hotels import HotelsRepository
from app.schemas import HotelResponse, HotelCreate, MessageResponse, HotelId

router = APIRouter(
    prefix="/hotels",
    tags=["Hotels"],
)


@router.post("/")
async def create_hotel(hotel_data: Annotated[HotelCreate, Depends()]) -> HotelId:
    hotel_id = await HotelsRepository.create_hotel(hotel_data)
    return {"ok": True, "hotel_id": hotel_id}


@router.get("/")
async def read_hotels() -> list[HotelResponse]:
    hotels = await HotelsRepository.get_hotels()
    return hotels


@router.put("/{hotel_id}")
async def update_hotels(hotel_id: int, hotel_data: Annotated[HotelCreate, Depends()]) -> MessageResponse:
    hotel_updated = await HotelsRepository.update_hotel(hotel_id, hotel_data)
    return hotel_updated


@router.delete("/{hotel_id}")
async def delete_hotels(hotel_id: int) -> MessageResponse:
    hotel_deleted = await HotelsRepository.delete_hotel(hotel_id)
    return hotel_deleted
