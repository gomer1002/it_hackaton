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

Запускаем проект

```
manager.py run
```

# База данных

## Таблица пользователей users

### Описание

Таблица users содержит данные о пользователях системы, такие как их уникальные идентификаторы, имена, контактные данные, роли и права доступа. Эта таблица служит основой для управления пользователями, их идентификацией и авторизацией в системе.

### Запрос создания таблицы

```
CREATE TABLE {tablename} (
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
    registered_on DATETIME NOT NULL,                        -- Дата создания
    registered_on_unix INT NOT NULL                         -- Юникс дата создания
);
```

## Таблица тем themes

### Описание

Таблица themes хранит информацию о темах заданий. Каждая тема имеет свой уникальный идентификатор, название, описание и дополнительные материалы. Эта таблица используется для организации и классификации заданий по темам.

### Запрос создания таблицы

```
CREATE TABLE tasks (
    task_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,     -- Идентификатор задания
    theme_id INTEGER NOT NULL,                              -- Идентификатор темы
    task_contributor VARCHAR(255) NOT NULL,                 -- Идентификатор создателя задания
    task_template TEXT NOT NULL,                            -- Текст шаблона задания
    task_additionals TEXT,                                  -- Дополнительные данные для шаблона
    timestamp DATETIME NOT NULL,                            -- Дата создания
    timestamp_unix INTEGER NOT NULL,                        -- Юникс дата создания
    FOREIGN KEY (theme_id) REFERENCES themes(theme_id)      -- Связь с таблицей themes
    FOREIGN KEY (task_contributor) REFERENCES users(uid)    -- Связь с таблицей users
);
```

## Таблица тем tasks

### Описание

Таблица tasks содержит информацию о заданиях, включая их уникальные идентификаторы, тексты шаблонов, дополнительные данные, даты создания и идентификаторы тем и создателей. Эта таблица является основной для управления заданиями и их атрибутами.

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
