

import sys
import os
import subprocess
import requests


API_KEY: str = open("xai.key", "r").read().strip()
GROK_URL: str = "https://api.x.ai/v1/chat/completions"
INIT_PROMPT: str = open("personal_prompt.key", "r").read().strip()
QUERY_FILE = "query.key"
EDITOR_ALIAS = "hx"


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


def open_with_editor(cleared: bool):
    if cleared:
        with open(QUERY_FILE, "w") as file:
            file.write("")
    subprocess.run([EDITOR_ALIAS, QUERY_FILE], check=True)


def main():
    grok = Grok()

    if not os.path.exists(QUERY_FILE):
        with open(QUERY_FILE, "w") as file:
            file.write("")

    print("opening helix to prompt Grok...")
    open_with_editor(QUERY_FILE)

    with open(QUERY_FILE, "r") as file:
        query = file.read().strip()

    if not query:
        print("no query provied, therefore exit")
        return

    full_query = INIT_PROMPT + " " + query

    response = grok.grok_query(full_query)
    print("\n", response)


if __name__ == '__main__':
    main()
