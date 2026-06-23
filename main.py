import os
import re
import requests

WEBHOOK_URL = os.environ["DISCORD_WEBHOOK"]

TARGET = "Sally___qq"
FILE_NAME = "last_tweet.txt"

url = f"https://x.com/{TARGET}"

response = requests.get(
    url,
    headers={
        "User-Agent": "Mozilla/5.0"
    },
    timeout=30
)

html = response.text

matches = re.findall(r'/status/(\d+)', html)

if not matches:
    raise Exception("ツイート取得失敗")

latest_id = matches[0]

try:
    with open(FILE_NAME, "r") as f:
        saved_id = f.read().strip()
except FileNotFoundError:
    saved_id = ""

# 初回実行
if saved_id == "":
    with open(FILE_NAME, "w") as f:
        f.write(latest_id)

    print("初回登録")
    exit()

# 新規投稿検知
if latest_id != saved_id:

    tweet_url = f"https://x.com/{TARGET}/status/{latest_id}"

    requests.post(
        WEBHOOK_URL,
        json={
            "content":
            f"【新しいポスト】\n{tweet_url}"
        },
        timeout=30
    )

    with open(FILE_NAME, "w") as f:
        f.write(latest_id)

    print("通知完了")

else:

    print("更新なし")
