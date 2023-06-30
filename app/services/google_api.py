from datetime import timedelta
from aiogoogle import Aiogoogle

from app.core.config import settings
from app.models import CharityProject
from app.services import constants as c


async def spreadsheet_create(wrapper_service: Aiogoogle) -> str:
    """
    Создаёт таблицу.

    ### Args:

        wrapper_service (Aiogoogle)

    ### Returns:
    Строка `id` созданной таблицы.
    """
    service = await wrapper_service.discover(
        api_name='sheets', api_version='v4'
    )
    spreadsheet_body = {
        'properties': {
            'title': c.TABLE_NAME,
            'locale': 'ru_RU'
        },
        'sheets': [
            {'properties': {
                'sheetType': 'GRID',
                'sheetId': 0,
                'title': c.SHEET_NAME_RATING_SPEED_CLOSING,
                'gridProperties': {
                    'rowCount': 50,
                    'columnCount': 5
                }
            }}
        ]
    }
    response: any = await wrapper_service.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return response['spreadsheetId']


async def set_user_permissions(
    spreadsheet_id: str,
    wrapper_service: Aiogoogle
) -> None:
    """
    Получает разрешение на доступ к таблице.

    ### Args:
    `id` таблицы.

        spreadsheet_id (str)

        wrapper_service (Aiogoogle)
    """
    permissions_body = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': settings.email
    }
    service = await wrapper_service.discover(
        api_name='drive',
        api_version='v3'
    )
    await wrapper_service.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields='id'
        )
    )


async def get_spreadsheet_id(wrapper_service: Aiogoogle) -> str:
    """
    Получает `id` таблицы. Создаёт новую, если таковой не существует.

    ### Args:

        wrapper_service (Aiogoogle)

    ### Returns:
    `id` таблицы.
    """
    service = await wrapper_service.discover(
        api_name='drive', api_version='v3'
    )
    response = await wrapper_service.as_service_account(
        service.files.list(
            q='mimeType="application/vnd.google-apps.spreadsheet"'
        )
    )

    spreadsheet_id = None
    table = response['files']

    if len(table) > 0:
        for spreadsheet in table:
            if spreadsheet['name'] == c.TABLE_NAME:
                spreadsheet_id = spreadsheet['id']
                break

    if spreadsheet_id is None:
        spreadsheet_id = spreadsheet_create(
            wrapper_service=wrapper_service
        )
    return spreadsheet_id


async def spreadsheet_update_value(
    spreadsheet_id: str,
    projects: list[CharityProject],
    wrapper_service: Aiogoogle
) -> None:
    """
    Обновляет данные таблицы.

    ### Args:
    Обновляемая таблица.

        spreadsheet_id (str):

    Список данных для обновления.

        projects (List[CharityProject])

        wrapper_service (Aiogoogle)
    """
    service = await wrapper_service.discover(
        api_name='sheets', api_version='v4'
    )
    await set_user_permissions(
        spreadsheet_id=spreadsheet_id,
        wrapper_service=wrapper_service
    )
    table_values = [[
        'Название проекта',
        'Затраченное время на сбор средств',
        'Описание'
    ]]
    for project in projects:
        table_values.append([
            project.name,
            str(timedelta(project.lifetime)),
            project.description
        ])

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    await wrapper_service.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range='A1:E30',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
