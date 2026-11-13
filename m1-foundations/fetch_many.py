"""Fetch 20 URLs concurrently, capped by an asyncio.Semaphore.

By default the script starts its own tiny HTTP server on 127.0.0.1 that waits
DELAY seconds before answering, so the timings are deterministic and nobody
else's site gets hit. Two of the 20 URLs ask that server for a 500 error, to
show that `gather(..., return_exceptions=True)` keeps the batch alive, and one
URL is "flaky" (500 on the first try only) to show the retry recovering.

A failed request (timeout, connection error or 5xx) is tried again once:
MAX_ATTEMPTS = 2 in total, with RETRY_DELAY seconds between them.

    uv run python m1-foundations/fetch_many.py              # limit 5
    uv run python m1-foundations/fetch_many.py --limit 1
    uv run python m1-foundations/fetch_many.py --limit 20
    uv run python m1-foundations/fetch_many.py --url https://httpbin.org/get
"""

import argparse
import asyncio
import time
from urllib.parse import parse_qs, urlsplit

import httpx

NUM_URLS = 20
DELAY = 0.5  # seconds the built-in server waits per request
FAIL_AT = {7, 13}  # these request indexes always get a 500
FLAKY_AT = {3}  # these get a 500 on the first attempt only
MAX_ATTEMPTS = 2  # total attempts per URL, so 1 retry
RETRY_DELAY = 0.2  # seconds to wait before retrying

seen_targets: set[str] = set()  # server-side memory for flaky URLs
retries = 0  # client-side count of retries, for the summary


# --- built-in local test server --------------------------------------------


async def handle(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    """Answer one HTTP request: sleep DELAY, then 200, or 500 for ?fail=1 and
    for the first hit on a ?flaky=1 URL."""
    request_line = (await reader.readline()).decode()
    while (await reader.readline()) not in (b"\r\n", b"\n", b""):
        pass  # skip headers

    target = request_line.split(" ")[1] if " " in request_line else "/"
    query = parse_qs(urlsplit(target).query)
    await asyncio.sleep(DELAY)

    first_hit = target not in seen_targets
    seen_targets.add(target)
    failed = query.get("fail") == ["1"] or (query.get("flaky") == ["1"] and first_hit)
    status = "500 Internal Server Error" if failed else "200 OK"
    body = f"{status} for {target}\n".encode()
    writer.write(
        f"HTTP/1.1 {status}\r\nContent-Length: {len(body)}\r\n"
        "Connection: close\r\n\r\n".encode() + body
    )
    await writer.drain()
    writer.close()


# --- client -----------------------------------------------------------------


def build_urls(base: str, local: bool) -> list[str]:
    """Return NUM_URLS URLs that differ only by query string."""
    urls = []
    for i in range(NUM_URLS):
        url = f"{base}?i={i}"
        if local and i in FAIL_AT:
            url += "&fail=1"
        if local and i in FLAKY_AT:
            url += "&flaky=1"
        urls.append(url)
    return urls


async def fetch(client: httpx.AsyncClient, sem: asyncio.Semaphore, url: str) -> float:
    """GET url (retrying on timeout, connection error or 5xx); return elapsed
    seconds of the successful attempt, or raise the last error.

    Each attempt takes its own semaphore slot, so the retry delay is spent
    outside the semaphore and doesn't block other requests.
    """
    global retries
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            async with sem:
                start = time.perf_counter()
                response = await client.get(url)
                response.raise_for_status()  # turn 4xx/5xx into an exception
                return time.perf_counter() - start
        except (httpx.TransportError, httpx.HTTPStatusError) as exc:
            # 4xx is our fault (bad URL, auth...), so retrying won't help.
            if isinstance(exc, httpx.HTTPStatusError) and exc.response.status_code < 500:
                raise
            if attempt == MAX_ATTEMPTS:
                raise
            retries += 1
            await asyncio.sleep(RETRY_DELAY)
    raise AssertionError("unreachable")


async def run(urls: list[str], limit: int) -> None:
    sem = asyncio.Semaphore(limit)
    async with httpx.AsyncClient(timeout=httpx.Timeout(10.0)) as client:
        start = time.perf_counter()
        results = await asyncio.gather(
            *(fetch(client, sem, u) for u in urls), return_exceptions=True
        )
        total = time.perf_counter() - start

    latencies = [r for r in results if isinstance(r, float)]
    errors = [(u, r) for u, r in zip(urls, results) if isinstance(r, BaseException)]

    print(f"Concurrency limit: {limit}")
    print(f"Requests:          {len(urls)}")
    print(f"Successes:         {len(latencies)}")
    print(f"Failures:          {len(errors)} (after {MAX_ATTEMPTS} attempts each)")
    print(f"Retries:           {retries}")
    for url, err in errors:
        print(f"  - {url}: {type(err).__name__}: {str(err).splitlines()[0]}")
    print(f"Total time:        {total:.2f} s")
    if latencies:
        avg = sum(latencies) / len(latencies)
        print(f"Avg per request:   {avg * 1000:.1f} ms (successful requests)")
    print(f"Avg wall / request: {total / len(urls) * 1000:.1f} ms (total / count)")


async def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--limit", type=int, default=5, help="semaphore size")
    parser.add_argument("--url", help="external base URL (default: built-in server)")
    args = parser.parse_args()

    if args.url:
        await run(build_urls(args.url, local=False), args.limit)
        return

    server = await asyncio.start_server(handle, "127.0.0.1", 0)
    port = server.sockets[0].getsockname()[1]
    async with server:
        await run(build_urls(f"http://127.0.0.1:{port}/item", local=True), args.limit)


if __name__ == "__main__":
    asyncio.run(main())
