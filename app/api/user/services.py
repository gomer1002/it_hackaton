from app import logger
from app.models.right import Right


def validate_update_data(post_data):
    try:
        uid = post_data.get("uid")
        first_name = post_data.get("first_name")
        last_name = post_data.get("last_name")
        email = post_data.get("email")
        rights = post_data.get("rights")
        if (
            isinstance(uid, str)
            and isinstance(first_name, str)
            and isinstance(last_name, str)
            and isinstance(email, str)
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
