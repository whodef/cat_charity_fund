# QRKot

[![Python](https://img.shields.io/badge/-Python3-464646?style=flat&logo=Python&logoColor=ffffff&color=informational)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/-FastAPI-464646?style=flat&logo=FastAPI&logoColor=ffffff&color=informational)](https://flask.palletsprojects.com/en/2.3.x/)
[![SQLAlchemy](https://img.shields.io/badge/-SQLAlchemy-464646?style=flat&logo=SQLAlchemy&logoColor=ffffff&color=informational)](https://www.sqlalchemy.org/)


## Описание

"QRKot" 

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
   APP_TITLE=<Название приложения>
   DESCRIPTION=<Описание проекта>
   DATABASE_URL=<Настройки подключения к БД, например: sqlite+aiosqlite:///./development.db>
   FIRST_SUPERUSER_EMAIL = <Ваш e-mail>
   FIRST_SUPERUSER_PASSWORD = <Ваш пароль>
   ```
   
5. Примените миграции
   ```angular2html
   alembic upgrade head
   ```
   
6. Запустите проект
   ```bash
   uvicorn app.main:app
   ```


## Полезные ссылки

[**Swagger Editor**](https://editor.swagger.io/)

## Автор проекта

**[Tatiana Seliuk](https://github.com/whodef)**