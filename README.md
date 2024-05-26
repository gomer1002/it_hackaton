# Цифровой помощник преподавателя

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# How to run:

Создаем витруальное окружение

```
py -m venv env
```

Запускаем виртуальное окружение

```
.\env\Scripts\activate
```

Устанавливаем необходимы для работы проекта пакеты

```
py -m pip install -r .\requirements.txt
```

Для установки может потребоваться Microsoft Visual C++ Build Tools. Необходимо будет скачать.

Создаем базу данных с тестовыми данными

```
py ./db_editod.py
```

Запускаем проект

```
py ./manage.py
```

Запускаем тесты

```
py ./app_test.py
```

В тестах описаны только спешные GET запросы на разные ресурсы API.

# База данных

## Таблица пользователей users

### Описание

Таблица users содержит данные о пользователях системы, такие как их уникальные идентификаторы, имена, контактные данные, роли и права доступа. Эта таблица служит основой для управления пользователями, их идентификацией и авторизацией в системе.

### Запрос создания таблицы

```
CREATE TABLE users (
    uid VARCHAR(255) PRIMARY KEY NOT NULL,                  -- Идентификатор пользователя
    photo VARCHAR(255),                                     -- Путь к фото
    first_name VARCHAR(255) NOT NULL,                       -- Имя
    last_name VARCHAR(255) NOT NULL,                        -- Фамилия
    father_name VARCHAR(255),                               -- Отчество
    email VARCHAR(255) UNIQUE NOT NULL,                     -- Email пользователя
    phone VARCHAR(255) UNIQUE,                              -- Телефон пользователя
    role VARCHAR(255) NOT NULL,                             -- Роль пользователя
    rights TEXT NOT NULL,                                   -- Список прав доступа
    department VARCHAR(255),                                -- Кафедра преподавателя
    description TEXT,                                       -- Описание
    password VARCHAR(255) NOT NULL,                         -- Пароль
    registered_on_unix INT NOT NULL                         -- Юникс дата создания
);
```

## Таблица заданий tasks

### Описание

Таблица tasks содержит информацию о заданиях, включая их уникальные идентификаторы, тексты шаблонов, дополнительные данные, даты создания и идентификаторы тем и создателей. Эта таблица является основной для управления заданиями и их атрибутами.

### Запрос создания таблицы

```
CREATE TABLE tasks (
    task_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,     -- Идентификатор задания
    theme_id INTEGER NOT NULL,                              -- Идентификатор темы
    task_contributor VARCHAR(255) NOT NULL,                 -- Идентификатор создателя задания
    task_template TEXT NOT NULL,                            -- Текст шаблона задания
    task_additionals TEXT,                                  -- Дополнительные данные для шаблона
    timestamp_unix INTEGER NOT NULL,                        -- Юникс дата создания
    FOREIGN KEY (theme_id) REFERENCES themes(theme_id)      -- Связь с таблицей themes
    FOREIGN KEY (task_contributor) REFERENCES users(uid)    -- Связь с таблицей users
);
```

## Таблица тем themes

### Описание

Таблица themes хранит информацию о темах заданий. Каждая тема имеет свой уникальный идентификатор, название, описание и дополнительные материалы. Эта таблица используется для организации и классификации заданий по темам.

### Запрос создания таблицы

```
CREATE TABLE themes (
    theme_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,        -- Идентификатор темы
    theme_name TEXT NOT NULL,                                   -- Название темы
    theme_description TEXT,                                     -- Описание темы
    theme_sources TEXT                                          -- Материалы по теме
);
```

## Связи

### Связь между tasks и themes:

Поле theme_id в таблице tasks является внешним ключом, ссылающимся на поле theme_id в таблице themes.
Отвечает за привязку заданий к определенным темам.

### Связь между tasks и users:

Поле task_contributor в таблице tasks является внешним ключом, ссылающимся на поле uid в таблице users.
Показывает какой пользователь создал задание.

# API документация

## Конечные точки API

### Модуль **auth**

#### Register User

- **Endpoint**: `/api/auth/register`
- **Method**: `POST`
- **Description**: Зарегистрировать нового пользователя.
- **Request Body**:
  - `email` (string): Адрес электронной почты пользователя.
  - `password` (string): Пароль пользователя.
  - `first_name` (string): Имя пользователя.
  - `last_name` (string): Фамилия пользователя.
- **Response**:
  - `200` (OK): Пользователь успешно создан.
  - `400` (Bad Request): Неверные данные запроса.
  - `409` (Conflict): Пользователь уже существует.

#### Login User

- **Endpoint**: `/api/auth/login`
- **Method**: `POST`
- **Description**: Авторизует пользователя.
- **Request Body**:
  - `email` (string): Адрес электронной почты пользователя.
  - `password` (string): Пароль пользователя.
- **Response**:
  - `200` (OK): Пользователь успешно вошел в систему.
  - `400` (Bad Request): Неверные данные запроса.
  - `401` (Unauthorized): Пользователь не найден или неверный пароль.

#### Logout User

- **Endpoint**: `/api/auth/logout`
- **Method**: `POST`
- **Description**: Деавторизует пользователя.
- **Request Headers**:
  - `Authorization` (string): JWT токен в формате "Bearer".
- **Response**:
  - `200` (OK): Выход из системы выполнен успешно.
  - `403` (Forbidden): Отсутствует заголовок Authorization.
  - `401` (Unauthorized): Неверный JWT токен.

### Модуль **user**

#### GET /api/user/get

- **Endpoint**: `/api/user/get`
- **Method**: `GET`
- **Description**: Извлекает список пользователей.
- **Request Headers**:
  - `Authorization` (string): JWT токен в формате "Bearer".
- **Response**:
  - **Status Codes**:
    - `200` (OK): Возвращает JSON-объект с данными пользователей.
    - `403` (Forbidden): Доступ запрещен.
    - `503` (Service Unavailable): Не удалось получить данные.

#### POST /api/user/set

- **Endpoint**: `/api/user/set`
- **Method**: `POST`
- **Description**: Добавляет нового пользователя.
- **Request Headers**:
  - `Authorization` (string): JWT токен в формате "Bearer".
- **Request Body**:
  - JSON-объект, содержащий данные пользователя.
- **Response**:
  - **Status Codes**:
    - `200` (OK): Пользователь создан.
    - `202` (Accepted): Ошибка в данных.
    - `400` (Bad Request): Требуются данные в формате JSON.
    - `403` (Forbidden): Доступ запрещен.
    - `503` (Service Unavailable): Не удалось создать пользователя.

#### POST /api/user/del

- **Endpoint**: `/api/user/del`
- **Method**: `POST`
- **Description**: Удаляет пользователя.
- **Request Headers**:
  - `Authorization` (string): JWT токен в формате "Bearer".
- **Request Body**:
  - JSON-объект, содержащий данные пользователя.
- **Response**:
  - **Status Codes**:
    - `200` (OK): Пользователь удален.
    - `202` (Accepted): Ошибка в данных.
    - `400` (Bad Request): Требуются данные в формате JSON.
    - `403` (Forbidden): Доступ запрещен.
    - `503` (Service Unavailable): Не удалось удалить пользователя.

#### GET /api/user/rights

- **Endpoint**: `/api/user/rights`
- **Method**: `GET`
- **Description**: Извлекает список прав.
- **Request Headers**:
  - `Authorization` (string): JWT токен в формате "Bearer".
- **Response**:
  - **Status Codes**:
    - `200` (OK): Возвращает JSON-объект с данными о правах.
    - `403` (Forbidden): Доступ запрещен.

### Модуль **task**

#### GET /api/task/get

- **Endpoint**: `/api/task/get`
- **Method**: `GET`
- **Description**: Извлекает задание или список заданий.
- **Request Headers**:
  - `Authorization` (string): JWT токен в формате "Bearer".
- **Response**:
  - **Status Codes**:
    - `200` (OK): Возвращает JSON-объект с данными заданий.
    - `403` (Forbidden): Доступ запрещен.
    - `503` (Service Unavailable): Не удалось получить данные.

#### POST /api/task/set

- **Endpoint**: `/api/task/set`
- **Method**: `POST`
- **Description**: Добавление нового задания.
- **Request Headers**:
  - `Authorization` (string): JWT токен в формате "Bearer".
- **Request Body**:
  - JSON-объект, содержащий данные пользователя.
- **Response**:
  - **Status Codes**:
    - `200` (OK): Изменения внесены.
    - `202` (Accepted): Необходимо передать JSON.
    - `400` (Bad Request): Неверные данные.
    - `403` (Forbidden): Доступ запрещен.
    - `500` (Service Unavailable): При обновлении данных возникла ошибка.

#### POST /api/task/update

- **Endpoint**: `/api/task/update`
- **Method**: `POST`
- **Description**: Обновление задания.
- **Request Headers**:
  - `Authorization` (string): JWT токен в формате "Bearer".
- **Request Body**:
  - JSON-объект, содержащий данные пользователя.
- **Response**:
  - **Status Codes**:
    - `200` (OK): Изменения внесены.
    - `202` (Accepted): Необходимо передать JSON.
    - `400` (Bad Request): Неверные данные.
    - `403` (Forbidden): Доступ запрещен.
    - `500` (Service Unavailable): При обновлении данных возникла ошибка.

#### GET /api/theme/get

- **Endpoint**: `/api/theme/get`
- **Method**: `GET`
- **Description**: Извлекает тему или список тем.
- **Request Headers**:
  - `Authorization` (string): JWT токен в формате "Bearer".
- **Response**:
  - **Status Codes**:
    - `200` (OK): Возвращает JSON-объект с данными тем.
    - `400` (Bad Request): Неверные данные.
    - `403` (Forbidden): Доступ запрещен.
    - `503` (Service Unavailable): Не удалось получить данные.

#### POST /api/theme/set

- **Endpoint**: `/api/theme/set`
- **Method**: `POST`
- **Description**: Добавление новой темы.
- **Request Headers**:
  - `Authorization` (string): JWT токен в формате "Bearer".
- **Request Body**:
  - JSON-объект, содержащий данные пользователя.
- **Response**:
  - **Status Codes**:
    - `200` (OK): Изменения внесены.
    - `202` (Accepted): Необходимо передать JSON.
    - `400` (Bad Request): Неверные данные.
    - `403` (Forbidden): Доступ запрещен.
    - `500` (Service Unavailable): При обновлении данных возникла ошибка.

#### POST /api/theme/update

- **Endpoint**: `/api/theme/update`
- **Method**: `POST`
- **Description**: Обновление темы.
- **Request Headers**:
  - `Authorization` (string): JWT токен в формате "Bearer".
- **Request Body**:
  - JSON-объект, содержащий данные пользователя.
- **Response**:
  - **Status Codes**:
    - `200` (OK): Изменения внесены.
    - `202` (Accepted): Необходимо передать JSON.
    - `400` (Bad Request): Неверные данные.
    - `403` (Forbidden): Доступ запрещен.
    - `500` (Service Unavailable): При обновлении данных возникла ошибка.

### Response Codes

- `200` (OK): Запрос выполнен успешно.
- `201` (Created): Запрос выполнен успешно, и был создан новый ресурс.
- `202` (Accepted): Запрос принят на обработку, но обработка еще не завершена. Клиент может проверить статус запроса позже.
- `204` (No Content): Запрос выполнен успешно, но нет данных для возврата.
- `400` (Bad Request): Сервер не может понять запрос.
- `401` (Unauthorized): Запрос требует аутентификации пользователя.
- `403` (Forbidden): Сервер понял запрос, но у пользователя нет прав доступа к запрашиваемому ресурсу.
- `404` (Not Found): Запрашиваемый ресурс не найден.
- `409` (Conflict): Запрос не может быть выполнен из-за конфликта с текущим состоянием целевого ресурса.
- `500` (Internal Server Error): Сервер столкнулся с неожиданной ошибкой, которая помешала выполнить запрос.
- `503` (Service Unavailable): Сервер временно не может обработать запрос из-за перегрузки или обслуживания. Это временное состояние, и клиент должен повторить запрос позже.
