"""pathlib file I/O plus a timer context manager written two ways.

    uv run python m1-foundations/files_and_context.py

Creates <repo>/data/ with sample.txt (and two small extra files so the glob
has something to filter). Every file is opened with `with open(...)` or via
Path.read_text()/write_text(), which open and close the file for you, so no
handle is ever left open.
"""

import time
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from types import TracebackType
from typing import Literal

REPO_ROOT = Path(__file__).resolve().parent.parent  # works from any cwd
DATA_DIR = REPO_ROOT / "data"
SAMPLE = DATA_DIR / "sample.txt"


# --- 1. Timer as a class ----------------------------------------------------


class Timer:
    """Context manager that prints how long its block took.

        with Timer("load"):
            ...
    """

    def __init__(self, label: str = "block") -> None:
        self.label = label
        self.elapsed = 0.0

    def __enter__(self) -> "Timer":
        self._start = time.perf_counter()
        return self  # bound to the name after `as`

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> Literal[False]:
        # Runs on normal exit AND when the block raises.
        self.elapsed = time.perf_counter() - self._start
        status = "" if exc_type is None else f" (raised {exc_type.__name__})"
        print(f"[Timer class] {self.label}: {self.elapsed:.6f} s{status}")
        return False  # False = don't swallow the exception, let it propagate


# --- 2. Timer with @contextmanager ------------------------------------------


@contextmanager
def timer(label: str = "block") -> Iterator[None]:
    """Same timer as a generator: code before `yield` is __enter__,
    code after it (in `finally`) is __exit__."""
    start = time.perf_counter()
    try:
        yield  # the body of the `with` block runs here
    finally:  # without finally, the print would be skipped if the block raises
        print(f"[@contextmanager] {label}: {time.perf_counter() - start:.6f} s")


# --- pathlib file I/O -------------------------------------------------------


def file_demo() -> None:
    print(f"Data dir: {DATA_DIR}")
    DATA_DIR.mkdir(parents=True, exist_ok=True)  # no error if it already exists

    # Write: Path.write_text opens, writes and closes in one call.
    SAMPLE.write_text("line 1: hello\nline 2: pathlib\nline 3: context managers\n", encoding="utf-8")

    # Append with an explicit `with open(...)`; the file closes when the block ends.
    with open(SAMPLE, "a", encoding="utf-8") as f:
        f.write("line 4: appended with open()\n")
    print(f"Handle closed after with-block: {f.closed}")

    # Extra files so the glob has something to match and something to skip.
    (DATA_DIR / "notes.txt").write_text("another text file\n", encoding="utf-8")
    (DATA_DIR / "table.csv").write_text("a,b\n1,2\n", encoding="utf-8")

    # Read, two ways.
    text = SAMPLE.read_text(encoding="utf-8")
    print(f"\nread_text() -> {len(text)} chars, {len(text.splitlines())} lines:")
    print(text, end="")

    with open(SAMPLE, encoding="utf-8") as f:
        first = f.readline().rstrip()
    print(f"First line via open(): {first!r}")

    # Path pieces.
    print(f"\nname={SAMPLE.name!r} stem={SAMPLE.stem!r} suffix={SAMPLE.suffix!r}")
    print(f"relative to repo: {SAMPLE.relative_to(REPO_ROOT).as_posix()}")

    # List *.txt (table.csv is not matched).
    print("\n*.txt in data/:")
    for path in sorted(DATA_DIR.glob("*.txt")):
        print(f"  {path.name:<12} {path.stat().st_size:>4} bytes")


def main() -> None:
    with Timer("file demo"):
        file_demo()

    with timer("sum of 1M ints"):
        total = sum(range(1_000_000))
    print(f"total = {total}")

    with Timer("sleep 0.1") as t:
        time.sleep(0.1)
    print(f"Timer object still has the result afterwards: t.elapsed = {t.elapsed:.3f} s")

    # Both timers still report when the block raises, and the error still propagates.
    print("\nWhen the block raises:")
    for make in (lambda: Timer("failing block"), lambda: timer("failing block")):
        try:
            with make():
                raise ValueError("boom")
        except ValueError as e:
            print(f"  caught outside the with: {e!r}")


if __name__ == "__main__":
    main()
