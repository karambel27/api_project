# FSTR Pereval API

REST API для добавления информации о горных перевалах.

## Стек

- Python
- Django
- Django REST Framework
- PostgreSQL

## Реализовано в первом спринте

- Создана база данных PostgreSQL.
- Созданы модели для пользователя, координат, уровня сложности, перевала и изображений.
- В таблицу перевалов добавлено поле status.
- При создании нового перевала status автоматически устанавливается в new.
- Реализован метод POST /submitData/.

## Запуск проекта

1. Установить зависимости:

pip install -r requirements.txt

2. Создать файл .env:

FSTR_DB_HOST=localhost
FSTR_DB_PORT=5432
FSTR_DB_NAME=fstr_db
FSTR_DB_LOGIN=fstr_user
FSTR_DB_PASS=fstr_password

3. Выполнить миграции:

python manage.py migrate

4. Запустить сервер:

python manage.py runserver

## Метод POST /submitData/

URL:

POST /submitData/

Метод принимает JSON с информацией о перевале и сохраняет данные в базу.

При успешном добавлении возвращает:

{
  "status": 200,
  "message": null,
  "id": 1
}