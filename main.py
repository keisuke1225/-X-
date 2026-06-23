import re
import requests

url = "https://x.com/Sally___qq"

response = requests.get(
    url,
    headers={
        "User-Agent": "Mozilla/5.0"
    },
    timeout=30
)

html = response.text

matches = re.findall(r'/status/(\d+)', html)

print("件数:", len(matches))

if matches:
    print("最新候補:", matches[0])
