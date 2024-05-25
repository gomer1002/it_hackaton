class Right:
    unverified = "unverified"

    read_users = "read_users"
    edit_users = "edit_users"
    read_teachers = "read_teachers"
    edit_teachers = "edit_teachers"

    access_user_panel = "access_user_panel"
    access_admin_panel = "access_admin_panel"
    access_teacher_panel = "access_teacher_panel"

    edit_tasks = "edit_tasks"

    @classmethod
    def get_list(cls):
        data = []
        for attrib in dir(cls):
            if attrib[:2] != "__" and attrib != "get_list":
                data.append(attrib)
        return data
