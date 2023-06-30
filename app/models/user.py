from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable

from app.core import db


class UserTable(SQLAlchemyBaseUserTable, db.Base):
    """Таблица `users`."""
    pass
