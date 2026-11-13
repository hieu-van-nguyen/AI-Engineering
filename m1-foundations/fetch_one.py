"""Fetch one URL with httpx.AsyncClient and print status code + elapsed time.

Default target is a local server, so nobody else's site gets hit:

    python -m http.server 8000      # in another terminal
    python m1-foundations/fetch_one.py

Pass a different URL as the first argument (e.g. https://httpbin.org/get).

A failed request (timeout, connection error or 5xx) is tried again once:
MAX_ATTEMPTS = 2 in total, with RETRY_DELAY seconds between them.
"""

import asyncio
import sys
import time

import httpx

DEFAULT_URL = "http://localhost:8000/"
MAX_ATTEMPTS = 2  # total attempts, so 1 retry
RETRY_DELAY = 0.5  # seconds to wait before retrying


async def get_with_retry(client: httpx.AsyncClient, url: str) -> httpx.Response:
    """GET url, retrying on timeout, connection error or 5xx. Raises the last error."""
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            response = await client.get(url)
            response.raise_for_status()  # 4xx/5xx -> HTTPStatusError
            return response
        except (httpx.TransportError, httpx.HTTPStatusError) as exc:
            # 4xx is our fault (bad URL, auth...), so retrying won't help.
            if isinstance(exc, httpx.HTTPStatusError) and exc.response.status_code < 500:
                raise
            if attempt == MAX_ATTEMPTS:
                raise
            print(f"Attempt {attempt} failed ({type(exc).__name__}), retrying in {RETRY_DELAY}s...")
            await asyncio.sleep(RETRY_DELAY)
    raise AssertionError("unreachable")


async def fetch_one(url: str) -> None:
    timeout = httpx.Timeout(10.0)  # 10s for connect, read, write and pool
    async with httpx.AsyncClient(timeout=timeout) as client:
        start = time.perf_counter()
        response = await get_with_retry(client, url)
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
        print(f"Timed out fetching {url} after {MAX_ATTEMPTS} attempts")
    except httpx.ConnectError:
        print(f"Could not connect to {url} after {MAX_ATTEMPTS} attempts (is the server running?)")
    except httpx.HTTPStatusError as exc:
        print(f"{url} returned HTTP {exc.response.status_code}")


if __name__ == "__main__":
    asyncio.run(main())
