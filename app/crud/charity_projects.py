from typing import Union

from sqlalchemy import asc, desc, select

from app.core import db
from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDCharityProject(CRUDBase):
    @staticmethod
    async def get_project_by_completion_rate(
            session: db.AsyncSession,
            reverse: bool = False
    ) -> Union[None, list]:
        """
        ### Gets:
        Получает отсортированный список закрытых проектов.

        ### Args:
        Объект сессии с БД.

            session (AsyncSession)

        Сортированного список по умолчанию начинается с наименьшего. Default's False

            reverse (bool):


        ### Returns:
        Отсортированный список проектов.

            List[CharityProject]
        """
        query = select(
            CharityProject.name,
            CharityProject.description,
            (db.datetime_func(CharityProject.close_date) -
             db.datetime_func(CharityProject.create_date)).label('lifetime')
        )

        query = (query.order_by(asc('lifetime')),
                 query.order_by(desc('lifetime')))[reverse]

        closed_projects = await session.execute(query)

        return closed_projects.all()


charity_projects_crud = CRUDCharityProject(CharityProject)
