import requests


def schedulePostInBackend(
    csrf_token: str, token: str, username: str, content: str, platform: str, date_time: str
):
    post_data = {
        "csrfmiddlewaretoken": csrf_token,
        "token": token,
        "username": username,
        "content": content,
        "provider": platform,
        "date_time": date_time
    }
    response = requests.post(f"http://127.0.0.1:8000/api/gists/", data=post_data)
    print(response.status_code)