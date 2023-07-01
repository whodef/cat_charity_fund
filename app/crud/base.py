from typing import Optional, Union

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation, User


class CRUDBase:
    """
    Базовый класс с CRUD.
    """
    def __init__(self, model):
        self.model = model

    async def get(self, obj_id: int, session: AsyncSession):
        query = select(self.model).where(self.model.id == obj_id)
        result = await session.execute(query)
        return result.scalars().first()

    async def get_multi(self, session: AsyncSession):
        query = select(self.model)
        results = await session.execute(query)
        return results.scalars().all()

    async def create(self, obj_in, session: AsyncSession, user: Optional[User] = None):
        obj_data = obj_in.dict()
        if user is not None:
            obj_data['user_id'] = user.id
        db_obj = self.model(**obj_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    @staticmethod
    async def update(existing_obj, obj_in, session: AsyncSession):
        existing_data = jsonable_encoder(existing_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in existing_data:
            if field in update_data:
                setattr(existing_obj, field, update_data[field])

        session.add(existing_obj)
        await session.commit()
        await session.refresh(existing_obj)
        return existing_obj

    @staticmethod
    async def remove(obj_to_delete, session: AsyncSession):
        await session.delete(obj_to_delete)
        await session.commit()
        return obj_to_delete

    @staticmethod
    async def get_object_id_by_name(
            object_name: str, model: Union[Donation, CharityProject], session: AsyncSession
    ) -> Optional[int]:
        query = select(model.id).where(model.name == object_name)
        result = await session.execute(query)
        return result.scalars().first()

    @staticmethod
    async def get_users_objects(
            user_id: int, model: Union[Donation, CharityProject], session: AsyncSession
    ):
        query = select(model).where(model.user_id == user_id)
        results = await session.execute(query)
        return results.scalars().all()
