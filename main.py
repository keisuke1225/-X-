import requests

url = "https://x.com/Sally___qq"

response = requests.get(
    url,
    headers={
        "User-Agent": "Mozilla/5.0"
    },
    timeout=30
)

print("status:", response.status_code)
print(response.text[:500])
