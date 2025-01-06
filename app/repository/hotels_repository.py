from fastapi import HTTPException
from sqlalchemy import select

from app.database import SessionDependency
from app.models import HotelORM
from app.schemas import HotelCreate, HotelResponse


class HotelsRepository:
    """
    Класс HotelsRepository используется для обработки операций с базой данных, связанных с отелем.
    """

    @classmethod
    async def create_hotel(cls, hotel_data: HotelCreate, session: SessionDependency) -> int:
        data = hotel_data.model_dump()
        new_hotel = HotelORM(**data)
        session.add(new_hotel)
        await session.flush()
        await session.commit()
        return new_hotel.id

    @classmethod
    async def get_hotels(cls, session: SessionDependency) -> list[HotelResponse]:
        query = select(HotelORM)
        result = await session.execute(query)
        hotel_models = result.scalars().all()
        return hotel_models

    @classmethod
    async def update_hotel(cls, hotel_id: int, hotel_data: HotelCreate, session: SessionDependency) -> dict:
        query = select(HotelORM).filter_by(id=hotel_id)
        result = await session.execute(query)
        hotel = result.scalar_one_or_none()
        if not hotel:
            raise HTTPException(status_code=404, detail="Hotel not found")

        for key, value in hotel_data.model_dump().items():
            setattr(hotel, key, value)

        await session.flush()
        await session.commit()
        return {"message": "Hotel updated successfully"}

    @classmethod
    async def delete_hotel(cls, hotel_id: int, session: SessionDependency) -> dict:
        query = select(HotelORM).filter_by(id=hotel_id)
        result = await session.execute(query)
        hotel = result.scalar_one_or_none()
        if not hotel:
            raise HTTPException(status_code=404, detail="Hotel not found")

        await session.delete(hotel)
        await session.commit()
        return {"message": "Hotel deleted successfully"}
