from typing import Union

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Donation, CharityProject


async def find_sources(
        session: AsyncSession,
        model: Union[Donation, CharityProject]
) -> list[Union[Donation, CharityProject]]:
    """
    Функция выполняет проверку на наличие незакрытых
    благотворительных проектов или пожертвований и возвращает
    список этих проектов/пожертвований, отсортированный по
    их ID в порядке добавления.
    """
    sources = await session.execute(
        select(model).where(
            model.fully_invested == 0).order_by(
                desc(model.id)))

    return sources.scalars().all()
