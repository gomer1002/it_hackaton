from app import logger

from app.models.services import get_db_connection
from sqlite3 import IntegrityError


class Theme:
    """
    Модель темы.
    """

    __tablename__ = "themes"

    def __init__(
        self, theme_id=None, theme_name=None, theme_description=None, theme_sources=None
    ):
        """Инициализация экземпляра класса темы.
        :return: None."""
        self.theme_id = theme_id
        self.theme_name = theme_name
        self.theme_description = theme_description
        self.theme_sources = theme_sources

    def serialize(self) -> dict:
        """Сериализация экземпляра класса в словарь.
        :return: dict."""
        data = {}
        if self.theme_id:
            data["theme_id"] = self.theme_id
        if self.theme_name:
            data["theme_name"] = self.theme_name
        if self.theme_description:
            data["theme_description"] = self.theme_description
        if self.theme_sources:
            data["theme_sources"] = self.theme_sources
        return data

    def save(self):
        """Запись темы в базу данных.
        :return: jwt токен или None."""
        try:
            theme = self.get_by_theme_id(self.theme_id)
            if theme is not None:
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
        """Обновление данных темы.
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

            query = f"UPDATE {self.__tablename__} SET {', '.join(fields)} WHERE uid = ?"

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
        :return: dict с данными о темах или None."""
        try:
            conn = get_db_connection()
            cur = conn.cursor()

            query = "SELECT * FROM {{self.__tablename__}}"

            cur.execute(query)
            themes = cur.fetchall()
            cur.close()
            conn.close()

            data = {}
            k = 0
            for ud in themes:
                data[k] = {
                    "theme_id": ud["theme_id"],
                    "theme_name": ud["theme_name"],
                    "theme_description": ud["theme_description"],
                    "theme_sources": ud["theme_sources"],
                }
                k += 1
            return data
        except ValueError as e:
            logger.error(str(e))
            return None

    @classmethod
    def get_by_theme_id(cls, theme_id):
        """Получение данных темы по ее theme_id.
        :return: dict с данными о теме или None."""
        try:
            conn = get_db_connection()
            cur = conn.cursor()

            query = f"SELECT * FROM {cls.__tablename__} WHERE theme_id = ?"

            cur.execute(query, (theme_id,))
            theme = cur.fetchone()
            cur.close()
            conn.close()
            return dict(theme) if theme else None
        except ValueError as e:
            logger.error(str(e))
            return None

    @classmethod
    def delete(cls, theme_id: str) -> bool | None:
        """Удаление темы из БД.
        :return: True или False."""
        try:
            conn = get_db_connection()
            cur = conn.cursor()

            query = f"DELETE FROM {cls.__tablename__} WHERE theme_id = ?"

            cur.execute(query, (theme_id,))
            conn.commit()
            cur.close()
            conn.close()
            return True
        except ValueError as e:
            logger.error(str(e))
            return None
