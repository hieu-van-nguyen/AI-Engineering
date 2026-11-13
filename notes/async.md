# Asynchronous Programming Notes

1. **Concurrency vs. Parallelism:** Concurrency is about managing multiple tasks seemingly at the same time (often interleaving execution), whereas parallelism is about executing multiple tasks simultaneously (requiring multiple CPU cores).
2. **The Event Loop:** The core mechanism in many async systems (like Node.js/Python asyncio); it monitors I/O operations, scheduling callbacks to run when asynchronous tasks complete, preventing the main thread from idling.
3. **Why `await` doesn't block:** When a task hits `await`, it *suspends* execution and yields control back to the event loop. This allows the loop to run other pending tasks instead of halting the entire program until the awaited I/O operation finishes.
4. **Threads/Processes:** Use threads or processes when your task is **CPU-bound** (e.g., heavy calculation, complex data processing). Since async mechanisms are optimized for I/O-bound tasks, blocking the CPU requires offloading to a separate OS thread or process.

## Semaphore experiment (`m1-foundations/fetch_many.py`, 2026-11-13)

20 requests to the script's built-in local server (0.5 s delay per request; 2 of the 20 return HTTP 500 on purpose).

| Semaphore limit | Total time | Avg per request | Successes / Failures |
|---|---|---|---|
| 1  | 10.31 s | 515.6 ms | 18 / 2 |
| 5  | 2.10 s  | 515.7 ms | 18 / 2 |
| 20 | 0.58 s  | 538.9 ms | 18 / 2 |

**Takeaway:** each request's own latency stays ~0.5 s no matter the limit; the semaphore only changes how many wait at once. Total ≈ ceil(20 / limit) × 0.5 s (20 → 4 → 1 "waves"). The 2 failures came back as exceptions in the `gather` results without cancelling the other 18 (`return_exceptions=True`).

### With retry (2 attempts, 0.2 s delay)

Added a "flaky" URL (500 on the first try only). Still 18 successes / 2 failures, but now the flaky one recovers and the 2 hard failures are retried once before giving up (3 retries total).

| Semaphore limit | Total time |
|---|---|
| 1  | 11.84 s |
| 5  | 2.62 s  |
| 20 | 1.31 s  |

Retries add a whole extra "wave" (delay + 0.5 s request) at the end, which is why limit 20 went from 0.58 s to 1.31 s.
