import sqlalchemy as sa

from app.core import db
from app.models.base import GenericFields


class CharityProject(db.Base, GenericFields):
    """
    Таблица для благотворительных проектов.

    ### Attrs:
    Первичный ключ.
        id (int)

    Описание проекта.

        description (str)

    Уникальное название проекта, длина от 1 до 100.

        name (str)


    Сумма должна быть больше 0.

        full_amount (int)

    Внесённая сумма. Default is 0.

        invested_amount (int):

    Собрана ли нужная сумма для проекта (закрыт ли проект). Default's False.

        fully_invested (bool)

    Дата создания проекта. Default's `datetime.now()`

        create_date (datetime)

    Дата закрытия проекта.

        close_date (datetime)
    """

    __table_args__ = (
        GenericFields.__table_args__ + (sa.CheckConstraint(
            'length(name) BETWEEN 1 AND 100',
            name='invalid length of name'
        ),)
    )

    name = sa.Column(
        sa.String(100),
        unique=True,
        nullable=False
    )

    description = sa.Column(
        sa.Text,
        nullable=False
    )
