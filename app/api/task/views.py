from flask import Blueprint, request
from flask.views import MethodView
from app.api.task.services import (
    validate_task_get_data,
    validate_task_post_data,
    validate_theme_get_data,
    get_data,
    validate_theme_post_data,
)
from app.services import response, response_auth, check_rights
from app.models.right import Right as R
from app.models.task import Task
from app.models.theme import Theme
from app.models.role import Role
from app.models.user import User

from flask_jwt_extended import jwt_required, get_jwt

task = Blueprint("task", __name__)
task_base_path = "/api/task"
theme_base_path = "/api/theme"


@task.route(f"{task_base_path}/get", methods=["GET"])
@jwt_required()
def get_task_item_view():
    """Получение задания или списка заданий.
    :return: Json ответ или сообщение об ошибке
    """
    claims = get_jwt()
    user_rights = claims.get("rights")
    # TODO check if rights is dict or list
    if R.unverified not in user_rights:
        task_id = request.values.get("task_id")
        theme_id = request.values.get("theme_id")
        if validate_task_get_data(task_id, theme_id):
            data = get_data(task_id, theme_id)
            return response(
                "success",
                "Данные успешно получены",
                200,
                data=data,
            )
        return response("failed", "Неверные данные", 400)
    return response("failed", "Доступ запрещен", 403)


@task.route(f"{task_base_path}/set", methods=["POST"])
@jwt_required()
def set_task_item_view():
    """Создание задания.
    :return: Json ответ или сообщение об ошибке
    """
    claims = get_jwt()
    user_rights = claims.get("rights")
    if check_rights(
        user_rights,
        or_rights=[R.access_admin_panel, R.access_teacher_panel],
        and_rights=[R.edit_tasks],
    ):
        if request.content_type == "application/json":
            post_data = request.get_json()
            if validate_task_post_data(post_data, create=True):
                result = Task(
                    theme_id=post_data.get("theme_id"),
                    task_contributor=claims.get("sub"),
                    task_template=post_data.get("task_template"),
                    task_additionals=post_data.get("task_additionals"),
                ).save()
                if result:
                    return response(
                        "success",
                        "Изменения внесены",
                        200,
                    )
                return response(
                    "failed",
                    "При обновлении данных возникла ошибка",
                    500,
                )
            return response("failed", "Неверные данные", 400)
        return response("failed", "Необходимо передать json", 202)
    return response("failed", "Доступ запрещен", 403)


@task.route(f"{task_base_path}/update", methods=["POST"])
@jwt_required()
def update_task_item_view():
    """Обновление задания.
    :return: Json ответ или сообщение об ошибке
    """
    claims = get_jwt()
    user_rights = claims.get("rights")
    if check_rights(
        user_rights,
        or_rights=[R.access_admin_panel, R.access_teacher_panel],
        and_rights=[R.edit_tasks],
    ):
        if request.content_type == "application/json":
            post_data = request.get_json()
            if validate_task_post_data(post_data, create=False):
                result = result = Task(
                    task_id=post_data.get("task_id"),
                    theme_id=post_data.get("theme_id"),
                    task_contributor=claims.get("sub"),
                    task_template=post_data.get("task_template"),
                    task_additionals=post_data.get("task_additionals"),
                ).save()
                if result:
                    return response("success", "Изменения внесены", 200)
                return response("failed", "При обновлении данных возникла ошибка", 500)
            return response("failed", "Неверные данные", 400)
        return response("failed", "Необходимо передать json", 202)
    return response("failed", "Доступ запрещен", 403)


@task.route(f"{theme_base_path}/get", methods=["GET"])
@jwt_required()
def get_theme_item_view():
    """Получение списка тем.
    :return: Json ответ или сообщение об ошибке
    """
    claims = get_jwt()
    user_rights = claims.get("rights")
    if check_rights(
        user_rights,
        or_rights=[R.access_admin_panel, R.access_teacher_panel],
        and_rights=[R.edit_tasks],
    ):
        get_data = request.values.to_dict()
        if validate_theme_get_data(get_data):
            if get_data.get("theme_id") is None:
                data = Theme.get()
            else:
                data = Theme.get_by_theme_id(
                    theme_id=get_data.get("theme_id"),
                )
            if isinstance(data, type(None)):
                return response("failed", "Не удалось получить данные", 503)
            return response(
                "success",
                "Данные успешно получены",
                200,
                data=data,
            )
        return response("failed", "Неверные данные", 400)
    return response("failed", "Доступ запрещен", 403)


@task.route(f"{theme_base_path}/set", methods=["POST"])
@jwt_required()
def set_theme_item_view():
    """Создание темы.
    :return: Json ответ или сообщение об ошибке
    """
    claims = get_jwt()
    user_rights = claims.get("rights")
    if check_rights(
        user_rights,
        or_rights=[R.access_admin_panel, R.access_teacher_panel],
        and_rights=[R.edit_tasks],
    ):
        if request.content_type == "application/json":
            post_data = request.get_json()
            if validate_theme_post_data(post_data, create=True):
                result = Theme(
                    theme_name=post_data.get("theme_name"),
                    theme_description=post_data.get("theme_description"),
                    theme_sources=post_data.get("theme_sources"),
                ).save()
                if result:
                    return response(
                        "success",
                        "Изменения внесены",
                        200,
                    )
                return response(
                    "failed",
                    "При обновлении данных возникла ошибка",
                    500,
                )
            return response("failed", "Неверные данные", 400)
        return response("failed", "Необходимо передать json", 202)
    return response("failed", "Доступ запрещен", 403)


@task.route(f"{theme_base_path}/update", methods=["POST"])
@jwt_required()
def update_theme_item_view():
    """Обновление темы.
    :return: Json ответ или сообщение об ошибке
    """
    claims = get_jwt()
    user_rights = claims.get("rights")
    if check_rights(
        user_rights,
        or_rights=[R.access_admin_panel, R.access_teacher_panel],
        and_rights=[R.edit_tasks],
    ):
        if request.content_type == "application/json":
            post_data = request.get_json()
            if validate_theme_post_data(post_data, create=True):
                result = Theme(
                    theme_id=post_data.get("theme_id"),
                    theme_name=post_data.get("theme_name"),
                    theme_description=post_data.get("theme_description"),
                    theme_sources=post_data.get("theme_sources"),
                ).save()
                if result:
                    return response(
                        "success",
                        "Изменения внесены",
                        200,
                    )
                return response(
                    "failed",
                    "При обновлении данных возникла ошибка",
                    500,
                )
            return response("failed", "Неверные данные", 400)
        return response("failed", "Необходимо передать json", 202)
    return response("failed", "Доступ запрещен", 403)
