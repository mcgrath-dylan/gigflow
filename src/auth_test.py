import requests

HEADERS = {"User-Agent": "gigflow/0.1"}

url = "https://www.reddit.com/r/forhire/new.json?limit=5"
response = requests.get(url, headers=HEADERS)

if response.status_code == 200:
    print("Connected successfully. Sample post titles:")
    posts = response.json()["data"]["children"]
    for post in posts:
        print(f"  - {post['data']['title']}")
else:
    print(f"Failed: HTTP {response.status_code}")
