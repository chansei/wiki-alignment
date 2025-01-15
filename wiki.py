import json
import os
import re
import base64

import requests
from requests.exceptions import Timeout


class Wiki:
    def __init__(self, wiki_id, api_id, secret):
        self.wiki_id = wiki_id
        header = {
            "Content-Type": "application/json",
        }
        contents = {
            "api_key_id": api_id,
            "secret": secret
        }
        try:
            r = requests.post(f"https://api.wikiwiki.jp/{self.wiki_id}/auth", headers=header, data=json.dumps(contents))
            self.token = json.loads(r.content)['token']
        except Timeout:
            self.token = None
            print("Timeout Error")

    def get_page(self, page_name):  # Get the page content
        header = {
            "Authorization": f"Bearer {self.token}"
        }
        try:
            r = requests.get(f"https://api.wikiwiki.jp/{self.wiki_id}/page/{page_name}", headers=header)
            return json.loads(r.content)
        except Exception:
            return None

    def put_page(self, page_name, text):  # Update the page content
        header = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        contents = {
            "source": text
        }
        try:
            r = requests.put(f"https://api.wikiwiki.jp/{self.wiki_id}/page/{page_name}", headers=header, data=json.dumps(contents))
            return r
        except Exception:
            return None

    def get_file_list(self, page_name):  # Show all attachments in the page
        header = {
            "Authorization": f"Bearer {self.token}"
        }
        try:
            r = requests.get(f"https://api.wikiwiki.jp/{self.wiki_id}/page/{page_name}/attachments", headers=header)
            return json.loads(r.content)
        except Exception:
            return None

    def put_file(self, page_name, file, file_name):  # Upload file to the page
        with open(file, "rb") as f:
            img = f.read()
            img = base64.b64encode(img).decode("utf-8")
        header = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        contents = {
            "filename": file_name,
            "data": img
        }
        try:
            r = requests.put(f"https://api.wikiwiki.jp/{self.wiki_id}/page/{page_name}/attachment", headers=header, data=json.dumps(contents))
            return r
        except Exception:
            return None


def main():
    return


if __name__ == '__main__':
    main()
