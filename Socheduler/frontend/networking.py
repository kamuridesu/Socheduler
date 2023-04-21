import requests


def schedulePostInBackend(
    csrf_token: str,
    token: str,
    username: str,
    content: str,
    provider: str,
    date_time: str,
):
    post_data = {
        "csrfmiddlewaretoken": csrf_token,
        "token": token,
        "username": username,
        "content": content,
        "provider": provider,
        "scheduled_date": date_time,
    }

    response = requests.post(f"http://127.0.0.1:8000/api/posts/", data=post_data)
    return response


def getAllScheduledPosts(tokens: list[dict]):
    responses: list[requests.Reponse] = []
    for info in tokens:
        token = info["token"]
        headers = {"Authorization": f"Token {token}"}

        response = requests.get("http://127.0.0.1:8000/api/posts/", headers=headers)

        print(response)
        if response.status_code == 200:
            responses.append(
                {"provider": info["provider"], "response": response.json()}
            )
    return responses
