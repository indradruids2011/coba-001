import asyncio
import os

import httpx
from dotenv import load_dotenv
from fake_useragent import UserAgent  # type: ignore

load_dotenv(override=True)
ua = UserAgent()


async def login(client: httpx.AsyncClient) -> None:
    url = "api/auth/auth/login"

    headers = {
        "user-agent": ua.random,
    }

    data = {
        "username": os.getenv("ANGGARAN_USERNAME"),
        "password": os.getenv("ANGGARAN_PASSWORD"),
        "id_daerah": os.getenv("ANGGARAN_ID_DAERAH"),
    }

    try:
        response = await client.post(url=url, headers=headers, data=data)
        response.raise_for_status()
        token = response.json()
        token = token["token"]
        print("Login berhasil")
        print("Token:", token)
    except httpx.HTTPError as e:
        print(f"Login gagal: {e}")


async def main() -> None:
    async with httpx.AsyncClient(
        base_url=str(os.getenv("ANGGARAN_BASE_URL")),
        verify=False,
        # to limit asynchronous concurrent connections limits can be applied:
        limits=httpx.Limits(max_connections=10),
        # tip: increase timeouts for concurrent connections:
        timeout=httpx.Timeout(60.0),
    ) as client:
        await login(client)


if __name__ == "__main__":
    asyncio.run(main())
