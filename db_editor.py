#
import sqlite3 as sl
from json import loads, dumps
from datetime import datetime as dt
import uuid

conf = loads(open("config.json", "r").read())


def get_connection():
    conn = sl.connect(conf.get("SQLITE_DATABASE_PATH"))
    conn.row_factory = sl.Row
    return conn


def create_users():
    # Подключение к базе данных
    conn = get_connection()
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
    conn = get_connection()
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
    conn = get_connection()
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


def add_test_records(uid):
    # Соединение с базой данных
    conn = get_connection()
    cursor = conn.cursor()

    # Добавление тестовых записей в таблицу themes
    themes = [
        ("Тема 1", "Описание темы 1", "Материалы по теме 1"),
        ("Тема 2", "Описание темы 2", "Материалы по теме 2"),
        ("Тема 3", "Описание темы 3", "Материалы по теме 3"),
        ("Тема 4", "Описание темы 4", "Материалы по теме 4"),
        ("Тема 5", "Описание темы 5", "Материалы по теме 5"),
    ]
    cursor.executemany(
        "INSERT INTO themes (theme_name, theme_description, theme_sources) VALUES (?, ?, ?)",
        themes,
    )

    # Получение theme_id для добавленных тем
    cursor.execute("SELECT theme_id FROM themes")
    theme_ids = [row[0] for row in cursor.fetchall()]

    # Добавление тестовых записей в таблицу tasks
    tasks = []
    for i in range(10):
        theme_id = theme_ids[i % len(theme_ids)]
        task_contributor = uid
        task_template = f"Текст шаблона задания {i + 1}"
        task_additionals = f"Дополнительные данные для шаблона {i + 1}"
        timestamp_unix = dt.now().timestamp()
        tasks.append(
            (
                theme_id,
                task_contributor,
                task_template,
                task_additionals,
                timestamp_unix,
            )
        )

    cursor.executemany(
        """
        INSERT INTO tasks (theme_id, task_contributor, task_template, task_additionals, timestamp_unix)
        VALUES (?, ?, ?, ?, ?)
    """,
        tasks,
    )

    # Сохранение изменений и закрытие соединения
    conn.commit()
    conn.close()


def create_superuser():
    # Данные суперпользователя по умолчанию
    email = "admin@mail.ru"
    password = "adminadmin"
    uid = str(uuid.uuid4())

    photo = None
    first_name = "Super"
    last_name = "Admin"
    father_name = "User"
    phone = "+1000000000"
    role = "admin"
    rights = [
        "read_users",
        "edit_users",
        "read_teachers",
        "edit_teachers",
        "access_user_panel",
        "access_admin_panel",
        "access_teacher_panel",
        "edit_tasks",
    ]
    rights_str = dumps({"0": rights})
    department = "Администрация"
    description = "Суперпользователь с полными правами"
    timestamp = dt.now().timestamp()

    # Подключение к базе данных
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()

        if user:
            print("Суперпользователь уже существует.")
        else:
            cursor.execute(
                """
                INSERT INTO users (uid, photo, first_name, last_name, father_name, email, phone, role, rights, department, description, registered_on_unix, password)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    uid,
                    photo,
                    first_name,
                    last_name,
                    father_name,
                    email,
                    phone,
                    role,
                    rights_str,
                    department,
                    description,
                    timestamp,
                    "$2a$12$.l2NoEUeph3n3pcSX0SCIeBcb8.Vy/gfYfxsMvEGVNtTvt6YZC9XO",
                ),
            )

            conn.commit()
            print("Суперпользователь успешно создан.")
    except sl.IntegrityError as e:
        print(f"Ошибка: {e}")
    finally:
        conn.close()
    return uid


if __name__ == "__main__":
    print(create_users())
    print(create_themes())
    print(create_tasks())
    # clear_users()
    uid = create_superuser()
    add_test_records(uid)

    pass
