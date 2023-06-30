import sqlalchemy
import fastapi_users_db_sqlalchemy as fastapi_users_sa

from app.core import db
from app.models.base import GenericFields


class Donation(db.Base, GenericFields):
    """
    Таблица пожертвований `donation`.

    ### Attrs:
    Первичный ключ.

        id (int)

    Foreign Key. id пользователя, сделавшего пожертвование.

        user_id (str)

    Необязательный текст комментария.

        comment (None | str)

    Сумма пожертвования. Больше 0.

        full_amount (int)

    Сумма из пожертвования, распределенная по проектам. Default's 0.

        invested_amount (int)

    Все ли деньги из пожертвования были распределены. Default's False.

        fully_invested (bool)

    Дата пожертвования. Default's `datetime.now()`

        create_date (datetime)

    Дата, когда вся сумма пожертвования была распределена.

        close_date (datetime)
    """

    user_id = sqlalchemy.Column(
        fastapi_users_sa.GUID, sqlalchemy.ForeignKey('user.id')
    )

    comment = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
