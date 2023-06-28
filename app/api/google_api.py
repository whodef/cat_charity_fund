from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends

from app import schemas
from app.core import user, db
from app.core.google_client import get_service
from app.services import google_api
from app.crud import charity_projects_crud as cpc
from app.services import constants as c

router = APIRouter()


@router.get(
    path='/',
    summary=c.GET_REPORT_TO_GOOGLE,
    response_model=schemas.GoogleAPIStringResponseSchema,
    dependencies=[Depends(user.current_superuser)]
)
async def get_report(
    session: db.AsyncSession = Depends(db.get_async_session),
    wrapper_service: Aiogoogle = Depends(get_service),
) -> dict[str, str]:
    """
    **Только для SuperUser.**
    Отправляет отчёт по скорости закрытия проектов в `googlesheets`.

    ### Gets:
    Возвращает URL-адрес изменённой таблицы.

    ### Args:
    Объект сессии с БД.

        session (db.AsyncSession, optional):
            Defaults to Depends(db.get_async_session)

    Асинхронный сервис работы с Google.

        wrapper_service (Aiogoogle, optional):
            Defaults to Depends(get_service)

    ### Returns:
        Dict:
            Ссылка на таблицу с данными.
    """
    closed_projects = await cpc.get_project_by_completion_rate(
        session=session
    )

    spreadsheet_id = await google_api.get_spreadsheet_id(
        wrapper_service=wrapper_service
    )

    await google_api.spreadsheet_update_value(
        spreadsheet_id=spreadsheet_id,
        projects=closed_projects,
        wrapper_service=wrapper_service
    )
    return {'url': f'https://docs.google.com/spreadsheets/d/{spreadsheet_id}'}
