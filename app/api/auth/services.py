from app import app, jwt_blocklist
from app.models.user import User

from flask_jwt_extended import get_jwt

import re


def validate_request_data(post_data, register=False):
    """Проверка полученных данных"""
    first_name = post_data.get("first_name") if register else "True"
    last_name = post_data.get("last_name") if register else "True"
    email = post_data.get("email")
    password = post_data.get("password")
    return (
        isinstance(first_name, str)
        and isinstance(last_name, str)
        and isinstance(password, str)
        and isinstance(email, str)
        and re.match(
            r"^[a-zA-Z0-9_.+-]+@(mail\.ru|gmail\.com|ya\.ru|yandex\.ru)$",
            email,
        )
    )


def register_user(post_data):
    """Регистрация пользователя с проверенными реквизитами"""
    user = User.get_by_email(email=post_data.get("email"))
    if isinstance(user, type(None)):
        jwt_token = User(
            first_name=post_data.get("first_name"),
            last_name=post_data.get("last_name"),
            email=post_data.get("email"),
            password=post_data.get("password"),
        ).save()
        return jwt_token
    return None


def auth_user(post_data):
    """Авторизация пользователя с проверенными реквизитами"""
    return User(
        email=post_data.get("email"), password=post_data.get("password")
    ).sign_in()


def blacklist_jwt_token(request_header):
    """Добавление jwt токена в черный список"""
    if request_header:
        jti = get_jwt()["jti"]
        jwt_blocklist.ttl(
            jti, "", app.config.get("JWT_ACCESS_TOKEN_EXPIRES").total_seconds()
        )
        return True
    return False
