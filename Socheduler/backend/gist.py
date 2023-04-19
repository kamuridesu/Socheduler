import json
import requests


def createGist(token: str, content: str) -> bool:
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': f'Bearer {token}',
        'X-GitHub-Api-Version': '2022-11-28',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = json.dumps({
        "description": "Schedule Test",
        "public": False,
        "files": {
            "SCHEDULED.txt": {
                "content": content
            }
        }
    }, separators=(',', ':'))

    response = requests.post('https://api.github.com/gists', headers=headers, data=data)
    if response.status_code == 201:
        return True
    return False
