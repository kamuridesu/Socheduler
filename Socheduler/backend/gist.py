import requests


class Gist:
    @staticmethod
    def createGist(token: str, content: str) -> bool:
        print(token)
        headers = {
            'Accept': 'application/vnd.github+json',
            'Authorization': f'Bearer {token}',
            'X-GitHub-Api-Version': '2022-11-28',
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        data = '{"description":"Example of a gist","public":false,"files":{"README.md":{"content":"Hello World"}}}'

        response = requests.post('https://api.github.com/gists', headers=headers, data=data)
        print(response)
        print(response.text)