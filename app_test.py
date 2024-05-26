import requests
import sys

cookie = {}
headers = {}
uid = ""


def app_login():
    data = {"email": "admin@mail.ru", "password": "adminadmin"}
    response = requests.post("http://localhost/api/auth/login", json=data)
    global cookie
    global headers
    cookie = {"access_token_cookie": response.json().get("access_token")}
    headers = {"Cookie": "; ".join(f"{k}={v}" for k, v in cookie.items())}

    print(f"{str(sys._getframe().f_code.co_name):40}\tOK")


def test_get_task_item_view():
    response = requests.get("http://localhost/api/task/get", headers=headers)
    data = response.json().get("data")
    assert response.status_code == 200
    assert response.json().get("status") == "success"
    assert response.json().get("message") == "Данные успешно получены"
    assert isinstance(data, dict)
    assert len(data) > 0

    print(f"{str(sys._getframe().f_code.co_name):40}\tOK")


def test_get_task_item_view_by_task_id():
    params = {"task_id": "5"}
    response = requests.get(
        "http://localhost/api/task/get", headers=headers, params=params
    )
    data = response.json().get("data")
    assert response.status_code == 200
    assert response.json().get("status") == "success"
    assert response.json().get("message") == "Данные успешно получены"
    assert isinstance(data, dict)
    assert len(data) > 0

    print(f"{str(sys._getframe().f_code.co_name):40}\tOK")


def test_get_task_item_view_by_theme_id():
    params = {"theme_id": "2"}
    response = requests.get(
        "http://localhost/api/task/get", headers=headers, params=params
    )
    data = response.json().get("data")
    assert response.status_code == 200
    assert response.json().get("status") == "success"
    assert response.json().get("message") == "Данные успешно получены"
    assert isinstance(data, dict)
    assert len(data) > 0

    print(f"{str(sys._getframe().f_code.co_name):40}\tOK")


def test_get_theme_item_view():
    response = requests.get("http://localhost/api/theme/get", headers=headers)
    data = response.json().get("data")
    assert response.status_code == 200
    assert response.json().get("status") == "success"
    assert response.json().get("message") == "Данные успешно получены"
    assert isinstance(data, dict)
    assert len(data) > 0

    print(f"{str(sys._getframe().f_code.co_name):40}\tOK")


def test_get_theme_item_view_by_theme_id():
    params = {"theme_id": "2"}
    response = requests.get(
        "http://localhost/api/theme/get", headers=headers, params=params
    )
    data = response.json().get("data")
    assert response.status_code == 200
    assert response.json().get("status") == "success"
    assert response.json().get("message") == "Данные успешно получены"
    assert isinstance(data, dict)
    assert len(data) > 0

    print(f"{str(sys._getframe().f_code.co_name):40}\tOK")


def test_get_user_item_view():
    global uid
    response = requests.get("http://localhost/api/user/get", headers=headers)
    data = response.json().get("data")
    uid = data.get(list(data)[0]).get("uid")
    assert response.status_code == 200
    assert response.json().get("status") == "success"
    assert response.json().get("message") == "Данные успешно получены"
    assert isinstance(data, dict)
    assert len(data) > 0
    assert isinstance(uid, str)

    print(f"{str(sys._getframe().f_code.co_name):40}\tOK")


def test_get_user_item_view_by_uid(uid):
    params = {"uid": uid}
    response = requests.get(
        "http://localhost/api/user/get", headers=headers, params=params
    )
    data = response.json().get("data")
    _uid = data.get("uid")
    assert response.status_code == 200
    assert response.json().get("status") == "success"
    assert response.json().get("message") == "Данные успешно получены"
    assert isinstance(data, dict)
    assert len(data) > 0
    assert isinstance(_uid, str)
    assert _uid == uid

    print(f"{str(sys._getframe().f_code.co_name):40}\tOK")


def test_get_user_rights_item_view():
    response = requests.get("http://localhost/api/user/rights", headers=headers)
    data = response.json().get("data")
    assert response.status_code == 200
    assert response.json().get("status") == "success"
    assert response.json().get("message") == "Данные успешно получены"
    assert isinstance(data, list)
    assert len(data) > 0

    print(f"{str(sys._getframe().f_code.co_name):40}\tOK")


if __name__ == "__main__":
    app_login()
    test_get_task_item_view()
    test_get_task_item_view_by_task_id()
    test_get_task_item_view_by_theme_id()
    test_get_theme_item_view()
    test_get_theme_item_view_by_theme_id()
    test_get_user_item_view()
    test_get_user_item_view_by_uid(uid)
    test_get_user_rights_item_view()

    print("All tests passed")
