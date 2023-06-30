
# For core.users

JWT_LIFE_TIME = 60 * 60


# For datetime.isoformat

TIMESPEC = 'seconds'


# For endpoints `api.charity_projects`

GET_ALL_CHARITY_PROJECTS = 'Просмотреть все благотворительные проекты'

CREATE_CHARITY_PROJECTS = 'Создать новый благотворительный проект'

UPDATE_CHARITY_PROJECT = 'Изменить благотворительный проект'

DELETE_CHARITY_PROJECTS = 'Удалить благотворительный проект'


# For endpoints `api.donations`

GET_ALL_DONATIONS = 'Просмотреть все пожертвования'

GET_MY_DONATIONS = 'Просмотреть все мои пожертвования'

CREATE_DONATION = 'Добавить пожертвование'


# For endpoints `api.google`

GET_REPORT_TO_GOOGLE = 'Добавить данные из БД в Google-таблицу'


# For googlesheets

TABLE_NAME = 'Отчеты по проекту QRkot'

SHEET_NAME_RATING_SPEED_CLOSING = 'Рейтинг проектов по скорости закрытия'


# For Error Messages

ERR_NO_DELETE_USER = 'Удаление пользователей запрещено!'

ERR_LEN_PASSWORD = 'Password should be at least 3 characters'

ERR_EMAIL_IN_PASSWORD = 'Пароль содержит Ваш e-mail!'

ERR_NAME_EXIST = 'Проект с таким именем уже существует!'

ERR_FULL_AMOUNT = 'Введённая сумма превышает уже инвестированную!'

ERR_HAS_INVEST = 'Удаление запрещено! В проект уже пожертвовано %s'

ERR_PROJECT_CLOSED = 'Закрытый проект нельзя редактировать!'

ERR_NOT_FOUND = 'Объект с таким id не найден.'

ERR_NO_TABLE_FIELD = 'Указанное поле отсутствует в таблице!'

ERR_BASE_INTEGRITY = 'Попытка записи некорректных данных в БД!'

ERR_BASE_ANY = 'Ошибка при соединении с БД!'


# Other Messages

USER_IS_SIGNED = 'Пользователь уже зарегистрирован'
