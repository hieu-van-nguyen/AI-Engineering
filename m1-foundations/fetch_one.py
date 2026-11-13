"""Fetch one URL with httpx.AsyncClient and print status code + elapsed time.

Default target is a local server, so nobody else's site gets hit:

    python -m http.server 8000      # in another terminal
    python m1-foundations/fetch_one.py

Pass a different URL as the first argument (e.g. https://httpbin.org/get).
"""

import asyncio
import sys
import time

import httpx

DEFAULT_URL = "http://localhost:8000/"


async def fetch_one(url: str) -> None:
    timeout = httpx.Timeout(10.0)  # 10s for connect, read, write and pool
    async with httpx.AsyncClient(timeout=timeout) as client:
        start = time.perf_counter()
        response = await client.get(url)
        elapsed = time.perf_counter() - start

    print(f"URL:     {url}")
    print(f"Status:  {response.status_code}")
    print(f"Bytes:   {len(response.content)}")
    print(f"Elapsed: {elapsed * 1000:.1f} ms")


async def main() -> None:
    url = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_URL
    try:
        await fetch_one(url)
    except httpx.TimeoutException:
        print(f"Timed out fetching {url}")
    except httpx.ConnectError:
        print(f"Could not connect to {url} (is the server running?)")


if __name__ == "__main__":
    asyncio.run(main())
