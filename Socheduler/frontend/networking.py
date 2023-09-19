import requests
import typing


def authorize(f: typing.Callable):
    def decorator(*args, **kwargs):
        uuid = kwargs.pop("uuid")
        return f(*args, **kwargs, headers={"Authorization": f"Token {uuid}"})

    return decorator


def schedulePostInBackend(
    csrf_token: str,
    uuid: str,
    token: str,
    username: str,
    content: str,
    provider: str,
    date_time: str,
):
    post_data = {
        "csrfmiddlewaretoken": csrf_token,
        "uuid": str(uuid),
        "token": token,
        "username": username,
        "content": content,
        "provider": provider,
        "scheduled_date": date_time,
    }

    response = requests.post(f"http://127.0.0.1:8000/api/posts/", data=post_data)
    return response


@authorize
def getAllScheduledPosts(headers: dict = {}):
    response = requests.get("http://127.0.0.1:8000/api/posts/", headers=headers)

    if response.status_code == 200:
        return response.json()


@authorize
def deleteScheduledPost(post_id: int, headers: dict = {}):
    response = requests.delete(
        f"http://127.0.0.1:8000/api/posts/{post_id}", headers=headers
    )
    return response.status_code == 204


@authorize
def getScheduledPost(post_id: int, headers: dict = {}):
    response = requests.get(
        f"http://127.0.0.1:8000/api/posts/{post_id}", headers=headers
    )
    if response.status_code == 200:
        return response.json()


@authorize
def updateScheduledPost(post_id: int, content: str, scheduled_date: str, csrf_token: str, headers: dict = {}):
    post_data = {
        "csrfmiddlewaretoken": csrf_token,
        "content": content,
        "scheduled_date": scheduled_date,
    }

    response = requests.put(
        f"http://127.0.0.1:8000/api/posts/{post_id}/", headers=headers, data=post_data)
    print(response)
