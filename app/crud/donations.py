from pydantic import UUID4

from app import models
from app.core import db
from app.crud.base import CRUDBase


class CRUDDonation(CRUDBase):
    async def get_my_donations(
        self,
        user_id: UUID4,
        session: db.AsyncSession
    ) -> list[models.Donation]:
        """
        ### Gets:
        Получает список пожертвований указанного пользователя.

        ### Args:
        `id` пользователя.

            user_id (UUID4)

        Объект сессии с БД.

            session (db.AsyncSession)


        ### Returns:
        Список пожертвований указанного пользователя.

            List[models.Donation]
        """
        return await super().get_by_field(
            required_field='user_id',
            value=user_id,
            session=session,
            one_obj=False
        )


donation_crud = CRUDDonation(models.Donation)
