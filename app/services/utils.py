from datetime import datetime

from app.core import db
from app.services import exceptions
from app.services import constants as c


async def try_commit_to_db(
    obj: db.Base,
    session: db.AsyncSession
) -> db.Base:
    """
    Записать данные в БД с обработкой ошибок.

    ### Args:
    Объект для записи в БД.

        `obj (db.Base)`

    Объект сессий с БД.

        `session (db.AsyncSession)`


    ### Raises:
    Записываемые данные не консистентны.

        `exceptions.HTTPExceptionInternalServerError`

    Иные ошибки при соединении с БД.

        `exceptions.HTTPExceptionInternalServerError`


    ### Returns:
        - db.Base:
            Записанный а БД объект.
    """
    try:
        await session.commit()
        await session.refresh(obj)
        return obj
    except exceptions.IntegrityError:
        raise exceptions.HTTPExceptionInternalServerError(
            detail=c.ERR_BASE_INTEGRITY
        )
    except Exception:
        raise exceptions.HTTPExceptionInternalServerError(
            detail=c.ERR_BASE_ANY
        )


def close_obj(obj: db.Base) -> None:
    """
    Закрывает объекты с распределёнными инвестициями.

    ### Args:
    Проверяемый объект.

       `obj (db.Base)`
    """
    obj.fully_invested = (obj.full_amount == obj.invested_amount)
    if obj.fully_invested:
        obj.close_date = datetime.now()


async def distribution_of_amounts(
    undivided: db.Base,
    crud_class: db.Base,
    session: db.AsyncSession
) -> None:
    """
    Все объекты должны иметь поля:
    `full_amount`, `invested_amount`,
    `fully_invested`, `created_date`.

    ### Args:
    Объект, содержащий поле `full_amount` из которого будет
    производится распределение.

        `undivided (CRUDBase)`

    Класс, имеющий метод `get_by_field`, возвращающий объекты,
    в которые возможно распределить сумму.

        `crud_class (CRUDBase)`

    Объект сессии с БД.

        `session (db.AsyncSession)`
    """
    receptions = await crud_class.get_for_distribution(
        session=session
    )
    for reception in receptions:
        needed = undivided.full_amount - undivided.invested_amount
        if not needed:
            break
        available = reception.full_amount - reception.invested_amount
        to_add = min(needed, available)
        reception.invested_amount += to_add
        undivided.invested_amount += to_add
        close_obj(reception)

    close_obj(undivided)

    await try_commit_to_db(
        obj=undivided,
        session=session
    )


def normalize_datetime(values: dict) -> dict:
    """
    Изменяет строковый формат даты в формат `ISO`.

    ### Args:
    Словарь с датами.

        values (dict)

    ### Returns:
    Словарь с уже отформатированными датами.
    """
    for date in ('create_date', 'close_date'):
        if values.get(date) is not None:
            values[date] = values[date].isoformat(
                timespec=c.TIMESPEC
            )
    return values
