from flask import Blueprint, request
from app.api.user.services import (
    validate_update_data,
)
from app.api.auth.services import (
    register_user,
    validate_request_data,
)
from app.services import response
from app.models.right import Right
from app.models.user import User

from flask_jwt_extended import jwt_required, get_jwt

user = Blueprint("user", __name__)


@user.route("/api/user/get", methods=["GET"])
@jwt_required()
def get_user_list_view():
    """Получение списка пользователей.
    :return: Json ответ или сообщение об ошибке
    """
    claims = get_jwt()
    user_rights = claims.get("rights")
    if Right.access_admin_panel in user_rights and Right.read_users in user_rights:
        uid = request.values.get("uid")
        data = {}
        if isinstance(uid, str):
            data = User.get_by_uid(uid)
        else:
            data = User.get()
        if data is None:
            return response("failed", "Не удалось получить данные", 503)
        return response(
            "success",
            "Данные успешно получены",
            200,
            data=data,
        )
    return response("failed", "Доступ запрещен", 403)


@user.route("/api/user/rights", methods=["GET"])
@jwt_required()
def get_rights_list_view():
    """Получение списка прав.
    :return: Json ответ или сообщение об ошибке
    """
    claims = get_jwt()
    user_rights = claims.get("rights")
    if Right.access_admin_panel in user_rights and Right.read_users in user_rights:
        data = Right.get_list()
        return response(
            "success",
            "Данные успешно получены",
            200,
            data=data,
        )
    return response("failed", "Доступ запрещен", 403)


@user.route("/api/user/update", methods=["POST"])
@jwt_required()
def update_existing_user_view():
    """Обновление пользователя.
    :return: Json ответ или сообщение об ошибке
    """
    claims = get_jwt()
    user_rights = claims.get("rights")
    logged_uid = claims.get("sub")
    if Right.access_admin_panel in user_rights and Right.edit_users in user_rights:
        if request.content_type == "application/json":
            data = request.get_json()
            if validate_update_data(data):
                if data["uid"] != logged_uid:
                    User(
                        uid=data["uid"],
                        photo_url=data["photo_url"],
                        first_name=data["first_name"],
                        last_name=data["last_name"],
                        father_name=data["father_name"],
                        phone=data["phone"],
                        email=data["email"],
                        password=data["password"],
                        department=data["department"],
                        description=data["description"],
                        role=data["role"],
                        rights=data["rights"],
                    ).save()
                    return response(
                        "success", "Данные пользователя успешно обновлены", 200
                    )
                return response(
                    "failed", "Невозможно изменить данные этого пользователя", 400
                )
            return response("failed", "Ошибка в данных", 202)
        return response("failed", "Необходимо передать json", 400)
    return response("failed", "Доступ запрещен", 403)


@user.route("/api/user/set", methods=["POST"])
@jwt_required()
def set_new_user_view():
    """Добавление пользователя.
    :return: Json ответ или сообщение об ошибке
    """
    claims = get_jwt()
    user_rights = claims.get("rights")
    if Right.access_admin_panel in user_rights and Right.edit_users in user_rights:
        if request.content_type == "application/json":
            data = request.get_json()
            if validate_request_data(data, register=True):
                token = register_user(data)
                if token:
                    return response("success", "Пользователь успешно создан", 200)
                return response("failed", "Пользователь уже существует", 202)
            return response("failed", "Ошибка в данных", 202)
        return response("failed", "Необходимо передать json", 400)
    return response("failed", "Доступ запрещен", 403)


@user.route("/api/user/del", methods=["POST"])
@jwt_required()
def del_user_view():
    """Удаление пользователя.
    :return: Json ответ или сообщение об ошибке
    """
    claims = get_jwt()
    user_rights = claims.get("rights")
    logged_uid = claims.get("sub")
    if Right.access_admin_panel in user_rights and Right.edit_users in user_rights:
        if request.content_type == "application/json":
            data = request.get_json()
            uid_for_del = data.get("uid")
            if isinstance(uid_for_del, str):
                if uid_for_del != logged_uid:
                    if User.delete(uid_for_del):
                        return response("success", "Пользователь успешно удален", 200)
                    return response("failed", "Не удалось удалить пользователя", 503)
                return response(
                    "failed", "Невозможно удалить данного пользователя", 400
                )
            return response("failed", "Необходимо передать uid", 400)
        return response("failed", "Необходимо передать json", 202)
    return response("failed", "Доступ запрещен", 403)
