from typing import Union
from datetime import datetime

from pydantic import (
    UUID4, BaseModel, Extra, Field, NonNegativeInt,
    PositiveInt, root_validator
)

from app.services import utils


class DonationBaseSchema(BaseModel):
    """
    Базовый класс схем данных для работы с `Donation`.

    ### Attrs:
    Сумма пожертвования должна быть больше 0.

        `full_amount`

    Комментарий к пожертвованию.

        `comment (str, optional)`
    """
    full_amount: PositiveInt = Field(..., example=591)
    comment: Union[None, str] = Field(
        None, example='Хочу помочь вашему проекту.'
    )

    class Config:
        extra = Extra.forbid


class DonationCreate(DonationBaseSchema):
    """
    Схема данных для создания нового пожертвования.

    ### Attrs:
    Необходимая сумма для закрытия проекта должна быть больше 0.

        `full_amount`

    Комментарий к пожертвованию.

        `comment (str, optional)`
    """
    pass


class DonationShortResponse(DonationBaseSchema):
    """
    Схема данных ответа.

    ### Attrs:
    Сумма пожертвования должна быть больше 0.

        `full_amount`

    Комментарий к пожертвованию.

        `comment (str, optional)`

    `id` пожертвования.

        `id (int)`

    Дата внесения пожертвования.

        `create_date (datetime)`
    """
    id: PositiveInt = Field(..., example=42)
    create_date: datetime = Field(
        ..., example='2023-05-21T17:42:13'
    )

    class Config:
        orm_mode = True

    @root_validator
    def normalize_datetime(cls, values: dict) -> dict:
        return utils.normalize_datetime(values=values)


class DonationLongResponse(DonationShortResponse):
    """
    Короткая схема данных для ответа.

    ### Attrs:
    Сумма пожертвования должна быть больше 0.

        `full_amount`

    Комментарий к пожертвованию.

        `comment (str, optional)`

    `id` пожертвования.

        `id (int)`

    Дата пожертвования.

        `create_date (datetime)`

    `id` пользователя, сделавшего пожертвование.

        `user_id (UUID4)`

    Сумма из пожертвования, распределённая по проектам.

        `invested_amount (int)`

    Распределены ли все средства из пожертвования.

        `fully_invested (bool)`

    Дата, когда вся сумма пожертвования была распределена.

        `close_date (None, datetime)`
    """
    user_id: UUID4 = Field(
        ...,
        example='6cc376e0-1c89-48ee-8ab9-9541ec216b94'
    )

    invested_amount: NonNegativeInt = Field(
        ..., example=591
    )

    fully_invested: bool = Field(
        ..., example=True
    )

    close_date: Union[None, datetime] = Field(
        None, example='2023-06-28T17:40:23'
    )
