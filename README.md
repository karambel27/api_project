# FSTR Pereval API

REST API для Федерации спортивного туризма России.
Проект реализует добавление информации о горных перевалах в базу данных.

## Стек технологий

* Python
* Django
* Django REST Framework
* PostgreSQL

## Реализовано в первом спринте

* Создана база данных PostgreSQL.
* Созданы модели для хранения данных:

  * User — пользователь;
  * Coords — координаты перевала;
  * Level — уровень сложности по сезонам;
  * PerevalAdded — информация о перевале;
  * Image — изображения перевала.
* В модель перевала добавлено поле `status`.
* При создании нового перевала статус автоматически устанавливается в `new`.
* Реализован REST API метод `POST /submitData/`.
* Данные для подключения к базе берутся из переменных окружения.

## Статусы модерации

Поле `status` может принимать значения:

* `new` — новая запись;
* `pending` — модератор взял запись в работу;
* `accepted` — модерация прошла успешно;
* `rejected` — информация не принята.

## Установка и запуск

Клонировать репозиторий:

```bash
git clone https://github.com/karambel27/api_project.git
cd api_project
```

Создать и активировать виртуальное окружение:

```bash
python -m venv venv
venv\Scripts\activate
```

Установить зависимости:

```bash
pip install -r requirements.txt
```

Создать файл `.env` в корне проекта:

```env
FSTR_DB_HOST=localhost
FSTR_DB_PORT=5432
FSTR_DB_NAME=fstr_db
FSTR_DB_LOGIN=fstr_user
FSTR_DB_PASS=your_password
```

Выполнить миграции:

```bash
python manage.py migrate
```

Запустить сервер:

```bash
python manage.py runserver
```

## API

### POST /submitData/

Добавляет новый перевал в базу данных.

URL:

```http
POST /submitData/
```

Пример успешного ответа:

```json
{
  "status": 200,
  "message": null,
  "id": 1
}
```

Пример ошибки:

```json
{
  "status": 400,
  "message": "Ошибка валидации данных",
  "id": null
}
```
