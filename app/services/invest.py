import datetime
from typing import Union

from app.models import CharityProject, Donation


def invest_money_into_project(
        target: Union[Donation, CharityProject],
        sources: list[Union[Donation, CharityProject]]
) -> None:
    """
    Функция распределяет свободные средства в благотворительные проекты.
    """
    needs_investing = target.full_amount
    changed_sources = []
    while needs_investing and sources:
        source = sources.pop()
        surplus = source.full_amount - source.invested_amount

        if surplus < needs_investing:
            changed_sources.append(source_set_fully_invested(source))
            needs_investing -= surplus
            target.invested_amount += surplus

        if surplus > needs_investing:
            source.invested_amount += needs_investing
            needs_investing = 0
        else:
            needs_investing = 0
            changed_sources.append(source_set_fully_invested(source))

    changed_sources.append(source_set_fully_invested(target))
    return changed_sources


def source_set_fully_invested(
        source: Union[Donation, CharityProject]) -> Union[Donation, CharityProject]:
    """
    Функция устанавливает для проекта или пожертвования
    статус 'fully_invested' и дату закрытия.
    """
    source.invested_amount = source.full_amount
    source.fully_invested = True
    source.close_date = datetime.datetime.now()
    return source
