from app import logger
from app.models.right import Right
from json import loads


def validate_update_data(post_data):
    try:

        uid = (post_data.get("uid"),)
        photo_url = (post_data.get("photo_url"),)
        first_name = (post_data.get("first_name"),)
        last_name = (post_data.get("last_name"),)
        father_name = (post_data.get("father_name"),)
        phone = (post_data.get("phone"),)
        email = (post_data.get("email"),)
        password = (post_data.get("password"),)
        department = (post_data.get("department"),)
        description = (post_data.get("description"),)
        role = (post_data.get("role"),)
        rights = loads(
            post_data.get("rights"),
        ).get("0")

        if (
            isinstance(uid, str)
            and (isinstance(photo_url, str) or photo_url is None)
            and isinstance(first_name, str)
            and isinstance(last_name, str)
            and (isinstance(father_name, str) or father_name is None)
            and (isinstance(phone, str) or phone is None)
            and isinstance(email, str)
            and (isinstance(password, str) or password is None)
            and (isinstance(department, str) or department is None)
            and (isinstance(description, str) or description is None)
            and isinstance(role, str)
            and isinstance(rights, list)
        ):
            actual_rights = Right.get_list()
            for each in rights:
                if each not in actual_rights:
                    return False
            return True
        return False
    except (ValueError, TypeError) as e:
        logger.error(str(e))
        return False
