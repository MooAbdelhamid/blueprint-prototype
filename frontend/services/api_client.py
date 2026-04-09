import requests

host = "http://127.0.0.1:8000"


def register_user(user, email, password):
    payload = {"user": user, "email": email, "password": password}
    url = host + "/register"
    response = requests.post(url, json=payload)

    print(response.status_code)
    print(response.json())
