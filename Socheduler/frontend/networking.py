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
        "scheduled_date": date_time
    }
    print(__import__("json").dumps(post_data))
    response = requests.post(f"http://127.0.0.1:8000/api/posts/", data=post_data)
    print(response.status_code)
    # print(response.content)