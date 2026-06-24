import os
import re
import requests

WEBHOOK_URL = os.environ["DISCORD_WEBHOOK"]

TARGET = "t_o_shimi_z"
FILE_NAME = "last_tweet.txt"

# 固定ツイートID
PINNED_ID = "2055281567451566450"

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

# 重複除去
tweet_ids = list(dict.fromkeys(matches))

# 固定ツイート除外
tweet_ids = [
    tweet_id
    for tweet_id in tweet_ids
    if tweet_id != PINNED_ID
]

if not tweet_ids:
    raise Exception("固定ツイート以外が取得できません")

# 一番大きいID = 最新ツイート
latest_id = max(tweet_ids, key=int)

print("latest_id =", latest_id)

# 前回保存したID取得
try:
    with open(FILE_NAME, "r") as f:
        saved_id = f.read().strip()
except FileNotFoundError:
    saved_id = ""

print("saved_id =", saved_id)

# 初回実行
if saved_id == "":
    with open(FILE_NAME, "w") as f:
        f.write(latest_id)

    print("初回登録完了")
    exit()

# 新規投稿検知
if latest_id != saved_id:

    tweet_url = f"https://x.com/{TARGET}/status/{latest_id}"

    r = requests.post(
        WEBHOOK_URL,
        json={
            "content": f"【{TARGET} 新規投稿】\n{tweet_url}"
        },
        timeout=30
    )

    print("Discord Status =", r.status_code)

    with open(FILE_NAME, "w") as f:
        f.write(latest_id)

    print("通知完了")

else:
    print("更新なし")
print(tweet_ids[:20])
