from fastapi import HTTPException
from sqlalchemy import select

from app.database import new_session
from app.models import HotelORM
from app.schemas import HotelCreate, HotelResponse


class HotelsRepository:
    """
    Класс HotelsRepository используется для обработки операций с базой данных, связанных с отелем.
    """
    @classmethod
    async def create_hotel(cls, hotel_data: HotelCreate) -> int:
        """
        Создание новой записи об отеле.

        Входной параметр:
        - hotel_data (HotelCreate): Содержит информацию о создаваемом отеле

        Возвращает:
        - int: идентификатор созданного отеля.
        """
        async with new_session() as session:
            data = hotel_data.model_dump()
            new_hotel = HotelORM(**data)
            session.add(new_hotel)
            await session.flush()
            await session.commit()
            return new_hotel.id

    @classmethod
    async def get_hotels(cls) -> list[HotelResponse]:
        """
        Получение всех данных об отелях.

        Возвращает:
        - list[HotelResponse]: 包含所有酒店信息的列表。
        """
        async with new_session() as session:
            query = select(HotelORM)
            result = await session.execute(query)
            hotel_models = result.scalars().all()
            return hotel_models

    @classmethod
    async def update_hotel(cls, hotel_id: int, hotel_data: HotelCreate) -> dict:
        """
        更新指定酒店的信息。

        参数:
        - hotel_id (int): 要更新的酒店的ID。
        - hotel_data (HotelCreate): 包含要更新的酒店信息。

        返回:
        - dict: 包含更新成功消息的字典。

        异常:
        - HTTPException: 如果找不到指定的酒店，抛出404异常。
        """
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

    @classmethod
    async def delete_hotel(cls, hotel_id: int, ) -> dict:
        """
        删除指定的酒店记录。

        参数:
        - hotel_id (int): 要删除的酒店的ID。

        返回:
        - dict: 包含删除成功消息的字典。

        异常:
        - HTTPException: 如果找不到指定的酒店，抛出404异常。
        """
        async with new_session() as session:
            query = select(HotelORM).filter_by(id=hotel_id)
            result = await session.execute(query)
            hotel = result.scalar_one_or_none()
            if not hotel:
                raise HTTPException(status_code=404, detail="Hotel not found")

            await session.delete(hotel)
            await session.commit()
            return {"message": "Hotel deleted successfully"}
