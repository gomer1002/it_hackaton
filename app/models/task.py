from app import logger

from app.models.services import get_db_connection
from sqlite3 import IntegrityError


class Task:
    """
    Модель задачи.
    """

    __tablename__ = "tasks"

    def __init__(
        self,
        task_id=None,
        theme_id=None,
        task_template=None,
        task_additionals=None,
        timestamp=None,
        timestamp_unix=None,
        task_contributor=None,
    ):
        """Инициализация экземпляра класса задачи.
        :return: None."""
        self.task_id = task_id
        self.theme_id = theme_id
        self.task_template = task_template
        self.task_additionals = task_additionals
        self.timestamp = timestamp
        self.timestamp_unix = timestamp_unix
        self.task_contributor = task_contributor

    def serialize(self) -> dict:
        """Сериализация экземпляра класса в словарь.
        :return: dict."""
        data = {}
        if self.task_id:
            data["task_id"] = self.task_id
        if self.theme_id:
            data["theme_id"] = self.theme_id
        if self.task_template:
            data["task_template"] = self.task_template
        if self.task_additionals:
            data["task_additionals"] = self.task_additionals
        if self.timestamp:
            data["timestamp"] = self.timestamp
        if self.timestamp_unix:
            data["timestamp_unix"] = self.timestamp_unix
        if self.task_contributor:
            data["task_contributor"] = self.task_contributor
        return data

    def save(self):
        """Запись задачи в базу данных.
        :return: jwt токен или None."""
        try:
            task = self.get_by_theme_id(self.theme_id)
            if task is not None:
                self.update()
            else:
                conn = get_db_connection()
                cur = conn.cursor()
                data = self.serialize()

                query = f"INSERT INTO {self.__tablename__} ({', '.join(data.keys())}) VALUES ({', '.join(['?'] * len(data.keys()))})"

                try:
                    cur.execute(query, list(data.values()))
                except IntegrityError as e:
                    logger.error(str(e))
                    return None

                conn.commit()
                cur.close()
                conn.close()
            return True
        except ValueError as e:
            logger.error(str(e))
            return None

    def update(self):
        """Обновление данных задачи.
        :return: True или False."""
        try:
            conn = get_db_connection()
            cur = conn.cursor()

            fields = []
            values = []
            for key, value in self.serialize():
                fields.append(f"{key} = ?")
                values.append(value)
            values.append(self.theme_id)

            query = (
                f"UPDATE {self.__tablename__} SET {', '.join(fields)} WHERE task_id = ?"
            )

            cur.execute(query, values)
            conn.commit()
            cur.close()
            conn.close()
            return True
        except ValueError as e:
            logger.error(str(e))
            return None

    @classmethod
    def get(cls):
        """Получение списка тем.
        :return: dict с данными о задачах или None."""
        try:
            conn = get_db_connection()
            cur = conn.cursor()

            query = f"SELECT * FROM {cls.__tablename__}"

            cur.execute(query)
            tasks = cur.fetchall()
            cur.close()
            conn.close()

            data = {}
            k = 0
            for ud in tasks:
                data[k] = {
                    "task_id": ud["task_id"],
                    "theme_id": ud["theme_id"],
                    "task_template": ud["task_template"],
                    "task_additionals": ud["task_additionals"],
                    "timestamp": ud["timestamp"],
                    "timestamp_unix": ud["timestamp_unix"],
                    "task_contributor": ud["task_contributor"],
                }
                k += 1
            return data
        except ValueError as e:
            logger.error(str(e))
            return None

    @classmethod
    def get_by_task_id(cls, task_id):
        """Получение данных задачи по ее task_id.
        :return: dict с данными о задаче или None."""
        try:
            conn = get_db_connection()
            cur = conn.cursor()

            query = f"SELECT * FROM {cls.__tablename__} WHERE task_id = ?"

            cur.execute(query, (task_id,))
            task = cur.fetchone()
            cur.close()
            conn.close()
            return dict(task) if task else None
        except ValueError as e:
            logger.error(str(e))
            return None

    @classmethod
    def get_by_theme_id(cls, theme_id):
        """Получение данных всех задач по theme_id.
        :return: dict с данными о задаче или None."""
        try:
            conn = get_db_connection()
            cur = conn.cursor()

            query = f"SELECT * FROM {cls.__tablename__} WHERE theme_id = ?"

            cur.execute(query, (theme_id,))
            tasks = cur.fetchall()
            cur.close()
            conn.close()

            data = {}
            k = 0
            for ud in tasks:
                data[k] = {
                    "task_id": ud["task_id"],
                    "theme_id": ud["theme_id"],
                    "task_template": ud["task_template"],
                    "task_additionals": ud["task_additionals"],
                    "timestamp": ud["timestamp"],
                    "timestamp_unix": ud["timestamp_unix"],
                    "task_contributor": ud["task_contributor"],
                }
                k += 1
            return data
        except ValueError as e:
            logger.error(str(e))
            return None

    @classmethod
    def delete(cls, task_id: str) -> bool | None:
        """Удаление задачи из БД.
        :return: True или False."""
        try:
            conn = get_db_connection()
            cur = conn.cursor()

            query = f"DELETE FROM {cls.__tablename__} WHERE task_id = ?"

            cur.execute(query, (task_id,))
            conn.commit()
            cur.close()
            conn.close()
            return True
        except ValueError as e:
            logger.error(str(e))
            return None
