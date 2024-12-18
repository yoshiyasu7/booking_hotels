from fastapi import HTTPException
from sqlalchemy import select

from app.database import new_session
from app.models import HotelORM
from app.schemas import HotelCreate, HotelResponse


class HotelsRepository:
    @staticmethod
    async def add_hotel(cls, hotel_data: HotelCreate) -> int:
        async with new_session() as session:
            data = hotel_data.model_dump()
            new_hotel = HotelORM(**data)
            session.add(new_hotel)
            await session.flush()
            await session.commit()
            return new_hotel.id

    @staticmethod
    async def get_hotels(cls) -> list[HotelResponse]:
        async with new_session() as session:
            query = select(HotelORM)
            result = await session.execute(query)
            hotel_models = result.scalars().all()
            hotels = [HotelResponse.model_validate(hotel_model) for hotel_model in hotel_models]
            return hotels

    @staticmethod
    async def update_hotel(cls, hotel_id: int, hotel_data: HotelCreate) -> dict:
        async with new_session() as session:
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

    @staticmethod
    async def delete_hotel(cls, hotel_id: int, ) -> dict:
        async with new_session() as session:
            query = select(HotelORM).filter_by(id=hotel_id)
            result = await session.execute(query)
            hotel = result.scalar_one_or_none()
            if not hotel:
                raise HTTPException(status_code=404, detail="Hotel not found")

            await session.delete(hotel)
            await session.commit()
            return {"message": "Hotel deleted successfully"}
