from app import logger
from app.models.task import Task


def validate_task_get_data(task_id, theme_id):
    """Проверка полученных данных"""
    try:
        return (isinstance(task_id, str) or task_id is None) and (
            isinstance(theme_id, str) or theme_id is None
        )
    except (ValueError, TypeError, KeyError) as e:
        logger.error(str(e))
        return False


def get_data(task_id, theme_id):
    """Получение данных"""
    try:
        if task_id is not None:
            return Task.get_by_task_id(task_id)
        elif theme_id is not None:
            return Task.get_by_theme_id(theme_id)
        else:
            return Task.get()

    except (ValueError, TypeError, KeyError) as e:
        logger.error(str(e))
        return None


def validate_task_post_data(post_data, create=False):
    """Проверка полученных данных"""
    try:
        if create:
            return (
                isinstance(post_data.get("theme_id"), str)
                and isinstance(post_data.get("task_template"), str)
                and (
                    isinstance(post_data.get("task_additionals"), str)
                    or post_data.get("task_additionals") is None
                )
            )
        else:
            return (
                isinstance(post_data.get("task_id"), str)
                and (
                    isinstance(post_data.get("theme_id"), str)
                    or post_data.get("theme_id") is None
                )
                and (
                    isinstance(post_data.get("task_template"), str)
                    or post_data.get("task_template") is None
                )
                and (
                    isinstance(post_data.get("task_additionals"), str)
                    or post_data.get("task_additionals") is None
                )
            )
    except (ValueError, TypeError, KeyError) as e:
        logger.error(str(e))
        return False


def validate_theme_get_data(get_data):
    """Проверка полученных данных"""
    try:
        return (
            isinstance(get_data.get("theme_id"), str)
            or get_data.get("theme_id") is None
        )
    except (ValueError, TypeError, KeyError) as e:
        logger.error(str(e))
        return False


def validate_theme_post_data(post_data, create=False):
    """Проверка полученных данных"""
    try:
        if create:
            return (
                isinstance(post_data.get("theme_name"), str)
                and isinstance(post_data.get("theme_description"), str)
                and (
                    isinstance(post_data.get("theme_sources"), str)
                    or post_data.get("theme_sources") is None
                )
            )
        else:
            return (
                isinstance(post_data.get("theme_id"), str)
                and isinstance(post_data.get("theme_name"), str)
                and (
                    isinstance(post_data.get("theme_description"), str)
                    or post_data.get("theme_description") is None
                )
                and (
                    isinstance(post_data.get("theme_sources"), str)
                    or post_data.get("theme_sources") is None
                )
            )
    except (ValueError, TypeError, KeyError) as e:
        logger.error(str(e))
        return False
