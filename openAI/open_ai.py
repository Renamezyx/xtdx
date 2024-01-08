# api doc:  https://platform.openai.com/docs/api-reference/making-requests

from requests import Response

from tools.request_base import request


class OpenAI(object):
    apis = {
        "completions": "https://api.openai.com/v1/chat/completions"
    }

    def __init__(self, api_key="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"):
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {0}".format(api_key)
        }

    def chat(self, content: str):
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "system",
                    "content": "中文"
                },
                {
                    "role": "user",
                    "content": content
                }
            ]
        }
        res: Response = request(method="post", url=self.apis["completions"], headers=self.headers, json=data)
        return res


if __name__ == '__main__':
    open_ai = OpenAI()
    open_ai.chat("hello")
