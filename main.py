import os
import asyncio
from twikit import Client

async def main():

    client = Client(language='ja')

    await client.login(
        auth_info_1=os.environ["X_USERNAME"],
        password=os.environ["X_PASSWORD"]
    )

    print("ログイン成功")

if __name__ == "__main__":
    asyncio.run(main())
