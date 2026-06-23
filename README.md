# FSTR Pereval API

REST API для Федерации спортивного туризма России.

Проект предназначен для хранения информации о горных перевалах, добавляемых пользователями через мобильное приложение.

---

# Стек технологий

* Python 3
* Django
* Django REST Framework
* PostgreSQL
* Git
* Postman

---

# Реализовано в первом спринте

## База данных

Создана база данных PostgreSQL.

Созданы модели:

* User — пользователь;
* Coords — координаты перевала;
* Level — уровень сложности перевала;
* PerevalAdded — информация о перевале;
* Image — фотографии перевала.

В модель перевала добавлено поле:

```text
status
```

Допустимые значения:

```text
new
pending
accepted
rejected
```

При создании нового перевала статус автоматически устанавливается в:

```text
new
```

---

## REST API

Реализован метод:

```http
POST /submitData/
```

Метод позволяет добавить новый перевал в базу данных.

---

## Переменные окружения

Для подключения к базе данных используются переменные окружения:

```env
FSTR_DB_HOST
FSTR_DB_PORT
FSTR_DB_NAME
FSTR_DB_LOGIN
FSTR_DB_PASS
```

---

# Реализовано во втором спринте

Добавлены методы получения и редактирования данных.

---

## Получение перевала по ID

### Запрос

```http
GET /submitData/<id>/
```

### Пример

```http
GET /submitData/1/
```

### Ответ

Возвращает полную информацию о перевале.

---

## Получение списка перевалов пользователя

### Запрос

```http
GET /submitData/?user__email=<email>
```

### Пример

```http
GET /submitData/?user__email=test@mail.ru
```

### Ответ

Возвращает список всех перевалов указанного пользователя.

Пример:

```json
[
    {
        "id": 1,
        "title": "Пхия",
        "status": "new"
    },
    {
        "id": 2,
        "title": "Клухор",
        "status": "accepted"
    }
]
```

---

## Редактирование перевала

### Запрос

```http
PATCH /submitData/<id>/
```

### Пример

```http
PATCH /submitData/1/
```

### Ограничения

Редактирование возможно только для записей со статусом:

```text
new
```

Если статус отличается от `new`, изменение данных запрещено.

Нельзя изменять данные пользователя:

* фамилию;
* имя;
* отчество;
* email;
* телефон.

---

### Успешный ответ

```json
{
    "state": 1,
    "message": null
}
```

### Ответ при ошибке

```json
{
    "state": 0,
    "message": "Редактировать можно только записи со статусом new."
}
```

---

# Структура API

| Метод | URL                              | Описание                                |
| ----- | -------------------------------- | --------------------------------------- |
| POST  | /submitData/                     | Добавление нового перевала              |
| GET   | /submitData/<id>/                | Получение перевала по ID                |
| PATCH | /submitData/<id>/                | Редактирование перевала                 |
| GET   | /submitData/?user__email=<email> | Получение списка перевалов пользователя |

---

# Установка проекта

Клонировать репозиторий:

```bash
git clone https://github.com/karambel27/api_project.git
cd api_project
```

Создать виртуальное окружение:

```bash
python -m venv venv
```

Активировать виртуальное окружение:

```bash
venv\Scripts\activate
```

Установить зависимости:

```bash
pip install -r requirements.txt
```

Создать файл `.env`:

```env
FSTR_DB_HOST=localhost
FSTR_DB_PORT=5432
FSTR_DB_NAME=fstr_db
FSTR_DB_LOGIN=fstr_user
FSTR_DB_PASS=your_password
```

Применить миграции:

```bash
python manage.py migrate
```

Запустить сервер:

```bash
python manage.py runserver
```

---

# Тестирование

Для тестирования API использовался Postman.

---
