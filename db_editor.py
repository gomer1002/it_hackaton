#
import sqlite3 as sl
from json import loads

conf = loads(open("config.json", "r").read())


def create_users():
    # Подключение к базе данных
    conn = sl.connect(conf.get("SQLITE_DATABASE_PATH"))
    conn.row_factory = sl.Row
    __tablename__ = "users"

    cur = conn.cursor()
    data = cur.execute(
        f"select count(*) from sqlite_master where type='table' and name='{__tablename__}'"
    )
    for row in data:
        # если таких таблиц нет
        if row[0] == 0:
            # создаём таблицу
            cur.execute(
                f"""
                    CREATE TABLE {__tablename__} (
                        uid VARCHAR(255) PRIMARY KEY NOT NULL,      -- Идентификатор пользователя
                        photo VARCHAR(255),                         -- Путь к фото
                        first_name VARCHAR(255) NOT NULL,           -- Имя
                        last_name VARCHAR(255) NOT NULL,            -- Фамилия
                        father_name VARCHAR(255),                   -- Отчество
                        email VARCHAR(255) UNIQUE NOT NULL,         -- Email пользователя
                        phone VARCHAR(255) UNIQUE,                  -- Телефон пользователя
                        role VARCHAR(255) NOT NULL,                 -- Роль пользователя
                        rights TEXT NOT NULL,                       -- Список прав доступа 
                        department VARCHAR(255),                    -- Кафедра преподавателя
                        description TEXT,                           -- Описание
                        password VARCHAR(255) NOT NULL,             -- Пароль
                        registered_on DATETIME NOT NULL,            -- Дата создания
                        registered_on_unix INT NOT NULL             -- Юникс дата создания
                    );
                """
            )
            conn.commit()
            cur.close()
            conn.close()
            return "\t".join(map(str, [__tablename__, True]))
        else:
            return "\t".join(map(str, [__tablename__, False]))


def create_tasks():
    # Подключение к базе данных
    conn = sl.connect(conf.get("SQLITE_DATABASE_PATH"))
    conn.row_factory = sl.Row
    __tablename__ = "tasks"

    cur = conn.cursor()
    data = cur.execute(
        f"select count(*) from sqlite_master where type='table' and name='{__tablename__}'"
    )
    for row in data:
        # если таких таблиц нет
        if row[0] == 0:
            # создаём таблицу
            cur.execute(
                f"""
                    CREATE TABLE {__tablename__} (
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
                """
            )
            conn.commit()
            cur.close()
            conn.close()
            return "\t".join(map(str, [__tablename__, True]))
        else:
            return "\t".join(map(str, [__tablename__, False]))


def create_themes():
    # Подключение к базе данных
    conn = sl.connect(conf.get("SQLITE_DATABASE_PATH"))
    conn.row_factory = sl.Row
    __tablename__ = "themes"

    cur = conn.cursor()
    data = cur.execute(
        f"select count(*) from sqlite_master where type='table' and name='{__tablename__}'"
    )
    for row in data:
        # если таких таблиц нет
        if row[0] == 0:
            # создаём таблицу
            cur.execute(
                f"""
                    CREATE TABLE {__tablename__} (
                        theme_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,        -- Идентификатор темы
                        theme_name TEXT NOT NULL,                                   -- Название темы
                        theme_description TEXT,                                     -- Описание темы
                        theme_sources TEXT                                          -- Материалы по теме
                    );
                """
            )
            conn.commit()
            cur.close()
            conn.close()
            return "\t".join(map(str, [__tablename__, True]))
        else:
            return "\t".join(map(str, [__tablename__, False]))


def clear_users():

    conn = sl.connect(conf.get("SQLITE_DATABASE_PATH"))
    conn.row_factory = sl.Row
    cur = conn.cursor()
    query = "DELETE FROM users"
    cur.execute(query)
    conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    print(create_users())
    print(create_themes())
    print(create_tasks())
    # clear_users()

    pass
