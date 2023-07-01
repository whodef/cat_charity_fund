from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Extra, Field, PositiveInt

from app.services import constants as c


class CharityProjectBase(BaseModel):
    """Базовый класс для работы с CharityProject."""
    name: Optional[str] = Field(
        None, min_length=c.CHARITY_PROJECT_MIN,
        max_length=c.CHARITY_PROJECT_NAME_MAX
    )
    description: Optional[str] = Field(
        None, min_length=c.CHARITY_PROJECT_MIN
    )
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    """Схема данных для создания нового благотворительного проекта."""
    name: str = Field(
        min_length=c.CHARITY_PROJECT_MIN,
        max_length=c.CHARITY_PROJECT_NAME_MAX)
    description: str = Field(min_length=c.CHARITY_PROJECT_MIN)
    full_amount: PositiveInt


class CharityProjectDB(CharityProjectCreate):
    """Схема данных, возвращаемых из БД."""
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True


class CharityProjectUpdate(CharityProjectBase):
    """Схема данных для обновления благотворительного проекта."""
    pass
