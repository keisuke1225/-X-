import os
import requests

WEBHOOK_URL = os.environ["DISCORD_WEBHOOK"]

requests.post(
    WEBHOOK_URL,
    json={
        "content": "Bot接続テスト成功！"
    }
)

print("送信完了")