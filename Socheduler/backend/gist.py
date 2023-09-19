"""## Gist related tasks

### funcs:
- createGist(token: str, content: str) -> bool:
    Creates a Gist for a user
"""

import json
import requests

from .models import PostModel


def createGist(pk: int, token: str, content: str) -> bool:
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = json.dumps(
        {
            "description": "Schedule Test",
            "public": False,
            "files": {"SCHEDULED.txt": {"content": content}},
        },
        separators=(",", ":"),
    )

    for _ in range(3):
        response = requests.post(
            "https://api.github.com/gists", headers=headers, data=data
        )
        if response.status_code == 201:
            try:
                post = PostModel.objects.get(pk=pk)
                post.is_published = True
                post.save()
            except PostModel.DoesNotExist:
                print("Post with pk " + str(pk) + " does not exists!")
                pass
            return {"error": False, "response": response.json()}
    return {"error": True, "response": response.text, "status": response.status_code}
