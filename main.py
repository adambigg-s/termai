

import sys
import requests


API_KEY: str = open("xai.key", "r").read().strip()
GROK_URL: str = "https://api.x.ai/v1/chat/completions"
INIT_PROMPT: str = open("personal_prompt.key", "r").read().strip()


class Grok:
    def __init__(self):
        pass

    def get_query(self) -> str:
        query = INIT_PROMPT + " " + " ".join(sys.argv[1:])
        return query

    def grok_query(self, query: str) -> str:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
        }
        data = {
            "model": "grok-beta",
            "messages": [
                {
                    "role": "user",
                    "content": query,
                }
            ]
        }
        ans = requests.post(GROK_URL, headers=headers, json=data)
        if ans.status_code == 200:
            return self.extract_first_response(ans)
        else:
            return f"error: {ans.status_code}, {ans.text}"

    def extract_first_response(self, ans) -> str:
        return ans.json()['choices'][0]['message']['content']


def main():
    grok = Grok()
    query = grok.get_query()
    reponse = grok.grok_query(query)

    print(reponse)


if __name__ == '__main__':
    main()
