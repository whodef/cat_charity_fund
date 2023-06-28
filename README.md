# QRKot

[![Python](https://img.shields.io/badge/-Python3-464646?style=flat&logo=Python&logoColor=ffffff&color=informational)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/-FastAPI-464646?style=flat&logo=FastAPI&logoColor=ffffff&color=informational)](https://flask.palletsprojects.com/en/2.3.x/)
[![SQLAlchemy](https://img.shields.io/badge/-SQLAlchemy-464646?style=flat&logo=SQLAlchemy&logoColor=ffffff&color=informational)](https://www.sqlalchemy.org/)


<img src="https://github.com/whodef/cat_charity_fund/assets/7266512/80b6078f-b95a-491d-b45b-5db1669836eb" alt="Pretty Cats" style="max-width: 100%;"/>


## Описание

Фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.

## Запуск проекта

1. Клонируйте репозиторий и перейдите в него
    ```bash
   https://github.com/whodef/cat_charity_fund.git
   ```
2. Установите и активируйте виртуальное окружение
    ```bash
   python3 -m venv venv
   ```
   
   * Если у вас Linux/MacOS: `source venv/bin/activate`
   
   * Если у вас Windows: `source venv/scripts/activate`


3. Установите зависимости из файла requirements.txt
    ```bash
    python3 -m pip install --upgrade pip
    ```
    ```bash
    pip3 install -r requirements.txt
    ```
   
4. Создайте в корне проекта файл .env с настройками
   ```bash
   APP_TITLE=QRKot
   DESCRIPTION=API проекта QRKot.
   VERSION=1.0.8
   DATABASE_URL=sqlite+aiosqlite:///./development.db
   FIRST_SUPERUSER_EMAIL=awedev@awe.dev
   FIRST_SUPERUSER_PASSWORD=AAA-DEADLINE-SOON-AAA
   ```
   
5. Примените миграции
   ```angular2html
   alembic upgrade head
   ```
   
6. Запустите проект
   ```bash
   uvicorn app.main:app --reload
   ```


## Полезные ссылки

[**Swagger Editor**](https://editor.swagger.io/)

## Автор проекта

**[Tatiana Seliuk](https://github.com/whodef)**
