from typing import Dict, List

from pydantic import BaseModel, Extra, Field, HttpUrl


class GoogleAPIBaseSchema(BaseModel):
    """
    Базовый класс схем данных для работы с `Google API`.

    ### Returns:
    Список проектов.

        `projects`
    """
    projects: List[Dict[str, str]] = Field(
        ...,
        example=[
            {
                'name': 'Для помощи определённым кошкам',
                'time_spent': '1 day, 10:15:44.123456',
                'description': 'Здесь должно быть описание'
            }
        ]
    )

    class Config:
        extra = Extra.forbid


class GoogleAPIStringResponseSchema(BaseModel):
    """
    Схема данных для ответа на запрос.

    ### Returns:
    Строка-ссылка на обработанный документ.

        url(HttpUrl)
    """
    url: HttpUrl = Field(
        ...,
        example='https://docs.google.com/spreadsheets/d/spreadsheet_id'
    )
