import bcrypt
import uuid

from app import app
from app import logger

from app.services import get_time
from app.models.services import get_db_connection
from app.models.role import Role
from app.models.right import Right
from flask_jwt_extended import create_access_token
from sqlite3 import IntegrityError
from json import dumps, loads


class User:
    """
    Модель пользователя.
    """

    __tablename__ = "users"

    def __init__(
        self,
        uid=None,
        photo_url=None,
        password=None,
        rights=None,
        role=None,
        first_name=None,
        last_name=None,
        father_name=None,
        phone=None,
        email=None,
        department=None,
        description=None,
    ):
        """Инициализация экземпляра класса пользователя.
        :return: None."""
        self.uid = uid if uid else str(uuid.uuid4())
        self.photo_url = photo_url
        self.first_name = first_name
        self.last_name = last_name
        self.father_name = father_name
        self.phone = phone
        self.email = email
        self.password = password
        self.department = department
        self.description = description
        self.role = role if role else Role.pupil
        self.rights = (
            rights
            if isinstance(rights, list)
            else [
                Right.access_user_panel,
                Right.place_order,
                Right.purchase_order,
            ]
        )
        self.registered_on = get_time()
        self.registered_on_unix = get_time(get_timestamp=True)

    def serialize(self, with_register=False) -> dict:
        """Сериализация экземпляра класса в словарь.
        :return: dict."""
        data = {}
        if self.uid:
            data["uid"] = self.uid
        if self.photo_url:
            data["photo_url"] = self.photo_url
        if self.first_name:
            data["first_name"] = self.first_name
        if self.last_name:
            data["last_name"] = self.last_name
        if self.father_name:
            data["father_name"] = self.father_name
        if isinstance(self.rights, list):
            data["rights"] = dumps({"0": self.rights})
        if self.role:
            data["role"] = self.role
        if self.phone:
            data["phone"] = self.phone
        if self.email:
            data["email"] = self.email
        if self.department:
            data["department"] = self.department
        if self.description:
            data["description"] = self.description
        if self.password:
            data["password"] = self._salt_password(self._pepper_password(self.password))
        if with_register:
            if self.registered_on:
                data["registered_on"] = self.registered_on
            if self.registered_on_unix:
                data["registered_on_unix"] = self.registered_on_unix
        return data

    def save(self):
        """Запись пользователя в базу данных.
        :return: jwt токен или None."""
        try:
            user = self.get_by_uid(self.uid)
            if user is not None:
                self.update()
            else:
                conn = get_db_connection()
                cur = conn.cursor()
                data = self.serialize(with_register=True)
                query = f"INSERT INTO users ({', '.join(data.keys())}) VALUES ({', '.join(['?'] * len(data.keys()))})"
                try:
                    cur.execute(query, list(data.values()))
                except IntegrityError as e:
                    logger.error(str(e))
                    return None
                print("ok")
                conn.commit()
                cur.close()
                conn.close()
            additional_claims = {
                "rights": self.rights,
                "role": self.role,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "father_name": self.father_name,
            }
            return create_access_token(
                identity=self.uid,
                additional_claims=additional_claims,
            )
        except ValueError as e:
            logger.error(str(e))
            return None

    def update(self):
        """Обновление данных пользователя.
        :return: True или False."""
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            fields = []
            values = []
            for key, value in self.serialize():
                fields.append(f"{key} = ?")
                values.append(value)
            values.append(self.uid)
            query = f"UPDATE users SET {', '.join(fields)} WHERE uid = ?"
            cur.execute(query, values)
            conn.commit()
            cur.close()
            conn.close()
            return True
        except ValueError as e:
            logger.error(str(e))
            return None

    def sign_in(self):
        """Проверка данных пользователя и генерация jwt токена.
        :return: jwt токен или None."""
        try:
            user = self.get_by_email(self.email)
            if isinstance(user, dict):
                db_password = user.get("password")
                candidate = self._pepper_password(self.password)
                if bcrypt.hashpw(candidate, db_password) == db_password:
                    uid = user["uid"]
                    additional_claims = {
                        "rights": loads(user["rights"])["0"],
                        "role": user["role"],
                        "first_name": user["first_name"],
                        "last_name": user["last_name"],
                        "father_name": user["father_name"],
                    }
                    return create_access_token(
                        identity=uid,
                        additional_claims=additional_claims,
                    )
            return None
        except ValueError as e:
            logger.error(str(e))
            return None

    @classmethod
    def get(cls):
        """Получение списка пользователей.
        :return: dict с данными о пользователе или None."""
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            query = "SELECT * FROM users"
            cur.execute(query)
            users = cur.fetchall()
            cur.close()
            conn.close()

            data = {}
            k = 0
            for ud in users:
                data[k] = {
                    "uid": ud["uid"],
                    "first_name": ud["first_name"],
                    "last_name": ud["last_name"],
                    "father_name": ud["father_name"],
                    "rights": loads(ud["rights"]["0"]),
                    "role": ud["role"],
                    "email": ud["email"],
                    "phone": ud["phone"],
                    "registered_on": ud["registered_on"],
                    "registered_on_unix": ud["registered_on_unix"],
                }
                k += 1
            return data
        except ValueError as e:
            logger.error(str(e))
            return None

    @classmethod
    def get_by_uid(cls, uid):
        """Получение данных пользователя по его id.
        :return: dict с данными о пользователе или None."""
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            query = "SELECT * FROM users WHERE uid = ?"
            cur.execute(query, (uid,))
            user = cur.fetchone()
            cur.close()
            conn.close()
            return dict(user) if user else None
        except ValueError as e:
            logger.error(str(e))
            return None

    @classmethod
    def get_by_phone(cls, phone: str) -> dict | None:
        """Получение данных пользователя по его телефону.
        :return: dict с данными о пользователе или None."""
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            query = "SELECT * FROM users WHERE phone = ?"
            cur.execute(query, (phone,))
            user = cur.fetchone()
            cur.close()
            conn.close()
            return dict(user) if user else None
        except ValueError as e:
            logger.error(str(e))
            return None

    @classmethod
    def get_by_email(cls, email: str) -> dict | None:
        """Получение данных пользователя по его email.
        :return: dict с данными о пользователе или None."""
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            query = "SELECT * FROM users WHERE email = ?"
            cur.execute(query, (email,))
            user = cur.fetchone()
            cur.close()
            conn.close()
            return dict(user) if user else None
        except ValueError as e:
            logger.error(str(e))
            return None

    @classmethod
    def delete(cls, uid: str) -> bool | None:
        """Удаление пользователя из БД.
        :return: True или False."""
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            query = "DELETE FROM users WHERE uid = ?"
            cur.execute(query, (uid,))
            conn.commit()
            cur.close()
            conn.close()
            return True
        except ValueError as e:
            logger.error(str(e))
            return None

    @classmethod
    def update(cls, data: dict) -> bool | None:
        """Обновление данных пользователя.
        :return: True или False."""
        return True

    @staticmethod
    def _pepper_password(password: str) -> str:
        """Добавление к паролю пользователя локального секретного ключа.
        :return: str: строка с локальным секретным ключом и исходной строкой."""
        pepper = app.config.get("PEPPER")
        return f"{password}{pepper}"
        # return f"{password}{pepper}".encode("utf-8")

    @staticmethod
    def _salt_password(password: str) -> str:
        """Добавление к паролю пользователя локального уникального ключа
        и хэширование пароля с помощью алгоритма bcrypt.
        :return: str: закодированная с помощью bcrypt строка."""
        return bcrypt.hashpw(
            password,
            bcrypt.gensalt(),
        )
