from typing import Union
from datetime import datetime

from pydantic import (
    BaseModel, Extra, Field, NonNegativeInt,
    PositiveInt, root_validator
)

from app.services import utils


class CharityProjectBaseSchema(BaseModel):
    """
    Базовый класс схем данных для работы с `CharityProject`.

    Название проекта. Длина от 1 до 100.

        `name (int, optional)`

    Описание проекта.

        `description (int, optional)`

    Необходимая сумма для закрытия проекта должна быть больше 0.

        `full_amount (int, optional)`
    """
    name: Union[None, str] = Field(
        None, min_length=1, max_length=100,
        example='Проект вселенского масштаба.',
    )

    description: Union[None, str] = Field(
        None, min_length=1,
        example='Собираем пожертвования для котиков!',
    )

    full_amount: Union[None, PositiveInt] = Field(None, example=5907)

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBaseSchema):
    """
    Схема данных для создания нового благотворительного проекта.

    ### Attrs:
    Название проекта. Длина от 1 до 100.

       `name (str)`

    Описание проекта.

        `description (str)`

    Необходимая сумма для закрытия проекта должна быть больше 0.

        `full_amount (int)`
    """
    name: str = Field(
        ...,
        example='Очень важный проект для котов.',
        min_length=1,
        max_length=100
    )
    description: str = Field(
        ...,
        example='Собираем немного тысяч денег для Мурзика!',
        min_length=1
    )
    full_amount: PositiveInt = Field(
        ...,
        example=5791
    )


class CharityProjectUpdate(CharityProjectBaseSchema):
    """
    Схема данных для обновления благотворительного проекта.

    ### Attrs:
    Название проекта. Длина от 1 до 100.

        `name (int, optional)`

    Описание проекта.

        `description (int, optional)`

    Необходимая сумма для закрытия проекта должна быть больше 0.

        `full_amount (int, optional)`
    """
    pass


class CharityProjectResponse(CharityProjectCreate):
    """
    Схема данных возвращаемых в ответе.

    ### Attrs:
    Название проекта. Длина от 1 до 100.

        `name (int)`

    Описание проекта.

        `description (str)`

    Необходимая сумма для закрытия проекта должна быть больше 0.

        `full_amount (int)`

    `id` проекта.

       `id (int)`

    Количество средств, внесённых в проект.

        `invested_amount (int)`

    Наполнен ли проект инвестициями.

        `fully_invested (bool)`

    Дата создания проекта.

        `create_date (datetime)`

    Дата закрытия проекта.

        `close_date (None, datetime)`
    """
    id: PositiveInt = Field(..., example=17)
    invested_amount: NonNegativeInt = Field(..., example=134)
    fully_invested: bool = Field(..., example=True)
    create_date: datetime = Field(..., example='2023-04-21T16:42:42')
    close_date: Union[None, datetime] = Field(None, example='2023-06-16T16:25:13')

    class Config:
        orm_mode = True

    @root_validator
    def normalize_datetime(cls, values: dict) -> dict:
        return utils.normalize_datetime(
            values=values
        )
