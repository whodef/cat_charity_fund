try:
    from app.core.config import settings
except (NameError, ImportError):
    raise AssertionError(
        'Не обнаружен инициализированный объект `settings`.'
        'Проверьте и поправьте: он должен быть доступен в модуле `app.core.config`',
    )
