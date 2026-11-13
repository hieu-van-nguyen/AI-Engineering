"""Async basics: sequential vs concurrent execution, and timeouts."""

import asyncio
import time


async def fetch(name: str, delay: float = 1) -> str:
    """Simulate an I/O-bound task."""
    print(f"  [{name}] start")
    await asyncio.sleep(delay)
    print(f"  [{name}] done")
    return f"{name} result"


async def run_sequential() -> None:
    print("Sequential:")
    start = time.perf_counter()
    await fetch("A")
    await fetch("B")
    print(f"  total: {time.perf_counter() - start:.2f}s (expected ~2s)\n")


async def run_gather() -> None:
    print("Concurrent (asyncio.gather):")
    start = time.perf_counter()
    results = await asyncio.gather(fetch("A"), fetch("B"))
    print(f"  results: {results}")
    print(f"  total: {time.perf_counter() - start:.2f}s (expected ~1s)\n")


async def run_timeout() -> None:
    print("Timeout (asyncio.timeout, 1s limit on a 5s task):")
    start = time.perf_counter()
    try:
        async with asyncio.timeout(1):
            await fetch("slow", delay=5)
    except TimeoutError:
        print("  slow task was cancelled by the timeout")
    print(f"  total: {time.perf_counter() - start:.2f}s (expected ~1s, not 5s)\n")


async def main() -> None:
    await run_sequential()
    await run_gather()
    await run_timeout()


if __name__ == "__main__":
    asyncio.run(main())
