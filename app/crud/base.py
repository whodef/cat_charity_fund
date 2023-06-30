from typing import Generic, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from sqlalchemy import asc, select

from app import schemas
from app.core import db
from app.services import utils
from app.services import constants as c

ModelType = TypeVar('ModelType', bound=db.Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=schemas.BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=schemas.BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Базовый класс CRUDBase."""
    def __init__(self, model: type[ModelType]) -> None:
        self.model = model

    async def get(
        self, obj_id: int,
        session: db.AsyncSession
    ) -> Union[None, ModelType]:
        """
        ### Gets:
        Получает объект из БД по `id`.

        ### Args:
        `id` искомого объекта.

            obj_id (int)

        Объект сессии с БД.

            session (db.AsyncSession)

        ### Returns:
        Найденный объект.

            None | ModelType
        """
        return await session.get(self.model, obj_id)

    async def get_all(self, session: db.AsyncSession) -> list[ModelType]:
        """
        ### Gets:
        Получает все объекты из запрошенной таблицы.

        ### Args:
        Объект сессии с БД.

            session (db.AsyncSession)

        ### Returns:
        Список объектов.

            list[ModelType]
        """
        objects = await session.scalars(
            select(self.model)
        )
        return objects.all()

    async def get_by_field(
        self, required_field: str,
        value: any, session: db.AsyncSession,
        one_obj: bool = True
    ) -> Union[ModelType, list[ModelType]]:
        """
        Находит объекты по значению указанного поля.

        ### Args:
        Поле, по которому ведётся поиск.

            field (str)

        Искомое значение.

            value (Any)

        Объект сессии с БД.

            session (db.AsyncSession)

        Вернуть один или все найденные объекты. Default's True.

            one_obj (bool, optional):

        По какому полю упорядочить запрос. Default's None.

            order_by (Union[None, str])

        ### Raises:
        Указанное поле отсутствует в таблице.

            raise AttributeError

        ### Returns:
        Найденные объекты.

            Union[ModelType, List[ModelType]]
        """
        field = getattr(self.model, required_field, None)

        if field is None:
            raise AttributeError(c.ERR_NO_TABLE_FIELD % required_field)

        query = select(self.model).where(field == value)

        if one_obj:
            return await session.scalar(query.limit(1))

        some_objs = await session.scalars(query)

        return some_objs.all()

    async def get_for_distribution(
        self, session: db.AsyncSession
    ) -> Union[ModelType, list[ModelType]]:
        """
        ### Gets:
        Получает все объекты с незакрытыми инвестициями.

        ### Args:
        Объект сессии с БД.

            session (db.AsyncSession)

        ### Returns:
        Найденные объекты.

            Union[ModelType, List[ModelType]]
        """
        objs = await session.scalars(
            select(self.model)
            .where(self.model.fully_invested.is_(False))
            .order_by(asc('create_date'))
        )
        return objs.all()

    async def create(
        self, new_obj: CreateSchemaType,
        session: db.AsyncSession,
        user: Union[None, schemas.UserDB] = None
    ) -> ModelType:
        """
        ### Posts:
        Создаёт запись в БД.

        ### Args:
        Данные для записи в БД.

            data (CreateSchemaType)

        Объект сессии.

            session (db.AsyncSession)

        Пользователь, создавший с запись. Default's None.

            user (None | schemas.UserDB, optional)

        ### Returns:
        Объект, записанный в БД.

            ModelType
        """
        new_obj = new_obj.dict()

        if user is not None:
            new_obj['user_id'] = user.id

        new_obj = self.model(**new_obj)
        session.add(new_obj)

        return await utils.try_commit_to_db(
            obj=new_obj,
            session=session
        )

    @staticmethod
    async def update(
        obj: ModelType, session: db.AsyncSession,
        update_data: UpdateSchemaType,
    ) -> ModelType:
        """
        Обновляет запись указанного объекта в БД.

        ### Args:
        Редактируемый объект.

            obj (ModelType)

        Объект сессии с БД.

            session (db.AsyncSession)

        Обновляемые данные.

            update_data (UpdateSchemaType)

        ### Returns:
        Обновлённый объект.

            ModelType
        """
        obj_data = jsonable_encoder(obj)

        update_data = update_data.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(obj, field, update_data[field])

        return await utils.try_commit_to_db(
            obj=obj,
            session=session
        )

    @staticmethod
    async def remove(obj: db.Base, session: db.AsyncSession) -> ModelType:
        """
        ### Remove:
        Удаляет запись из БД.

        ### Args:
        Удаляемый объект.

            obj (db.Base)

        Объект сессии.

            session (db.AsyncSession)

        ### Returns:
        Данные объекта всё ещё хранятся в сессии после удаления из БД. Удалённый объект.

            ModelType
        """
        await session.delete(obj)
        await session.commit()
        return obj
