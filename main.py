import os
import re
import requests
from playwright.sync_api import sync_playwright

WEBHOOK_URL = os.environ["DISCORD_WEBHOOK"]

TARGET = "t_o_shimi_z"
FILE_NAME = "last_tweet.txt"

with sync_playwright() as p:

    browser = p.chromium.launch(headless=True)

    page = browser.new_page()

    page.goto(
        f"https://x.com/{TARGET}",
        wait_until="networkidle",
        timeout=60000
    )

    html = page.content()

    browser.close()

matches = re.findall(r'/status/(\d+)', html)

if not matches:
    raise Exception("ツイート取得失敗")

tweet_ids = list(dict.fromkeys(matches))

latest_id = max(tweet_ids, key=int)

print("latest_id =", latest_id)

try:
    with open(FILE_NAME, "r") as f:
        saved_id = f.read().strip()
except FileNotFoundError:
    saved_id = ""

print("saved_id =", saved_id)

if saved_id == "":
    with open(FILE_NAME, "w") as f:
        f.write(latest_id)

    print("初回登録完了")
    exit()

if latest_id != saved_id:

    tweet_url = f"https://x.com/{TARGET}/status/{latest_id}"

    r = requests.post(
        WEBHOOK_URL,
        json={
            "content":
            f"【新しいポスト】\n{tweet_url}"
        },
        timeout=30
    )

    print("Discord =", r.status_code)

    with open(FILE_NAME, "w") as f:
        f.write(latest_id)

    print("通知完了")

else:
    print("更新なし")
