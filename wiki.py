import json
import os

import requests
from requests.exceptions import Timeout
from urllib3 import Timeout


def api_auth(url, pwd):
    header = {
        "Content-Type" : "application/json",
        "password" : ""
    }
    header['password'] = pwd
    try:
        r = requests.post(url, json=header, timeout=3.0)
        return json.loads(r.content)
    except Exception:
        return None

def api_get(url, token):
    header = {
        "Authorization" : "Bearer "
    }
    header['Authorization'] += token
    try:
        r = requests.get(url, headers=header)
        return json.loads(r.content)
    except Exception:
        return None    

def api_put(url, token, text):
    header = {
        "Authorization" : "Bearer ",
        "Content-Type" : "application/json"
    }
    header['Authorization'] += token
    contents = {
        "source" : text
    }
    try:
        r = requests.put(url, headers=header, data=json.dumps(contents))
        return r
    except Exception:
        return None

def main():
    return

if __name__ == '__main__':
    main()
