"""Pydantic v2 basics with a small Ticket model.

Covers: validating good data, catching ValidationError for bad data,
a JSON round-trip, and a custom field_validator.

    uv run python m1-foundations/pydantic_basics.py
"""

import json
from typing import Any, Literal

from pydantic import BaseModel, ValidationError, field_validator


class Ticket(BaseModel):
    id: int
    title: str
    priority: Literal["low", "medium", "high"]
    tags: list[str] = []  # safe in Pydantic: each instance gets its own copy

    @field_validator("title")
    @classmethod
    def title_not_blank(cls, value: str) -> str:
        """Reject empty or whitespace-only titles, and trim the rest."""
        if not value.strip():
            raise ValueError("title must not be blank")
        return value.strip()


def section(name: str) -> None:
    print(f"\n=== {name} ===")


def try_validate(label: str, data: dict[str, Any]) -> None:
    """Validate data and print either the ticket or the error list."""
    print(f"\n-- {label}: {data}")
    try:
        ticket = Ticket.model_validate(data)
        print(f"OK: {ticket!r}")
    except ValidationError as e:
        print(f"ValidationError ({e.error_count()} error(s)):")
        for err in e.errors():
            # each err is a dict: type, loc, msg, input (+ ctx/url)
            print(f"  type={err['type']!r} loc={err['loc']} msg={err['msg']!r} input={err['input']!r}")


def main() -> None:
    section("Good data")
    ticket = Ticket.model_validate(
        {"id": 1, "title": "  Login page is slow  ", "priority": "high", "tags": ["perf", "auth"]}
    )
    print(repr(ticket))
    # Lax mode coerces obvious matches: "2" -> 2, and tags falls back to the default.
    print(repr(Ticket.model_validate({"id": "2", "title": "Typo on homepage", "priority": "low"})))

    section("Bad data")
    try_validate("wrong type", {"id": "abc", "title": "Crash on save", "priority": "low"})
    try_validate("missing field", {"id": 3, "priority": "medium"})
    try_validate("invalid priority", {"id": 4, "title": "Dark mode", "priority": "urgent"})
    try_validate("blank title (field_validator)", {"id": 5, "title": "   ", "priority": "low"})
    try_validate("several problems at once", {"id": None, "priority": "LOW", "tags": "x"})

    section("JSON round-trip")
    as_json = ticket.model_dump_json()
    print(f"model_dump_json(): {as_json}")
    restored = Ticket.model_validate_json(as_json)
    print(f"model_validate_json(): {restored!r}")
    print(f"restored == original: {restored == ticket}")
    print(f"model_dump() (dict):   {ticket.model_dump()}")
    print(f"pretty JSON:\n{json.dumps(json.loads(as_json), indent=2)}")


if __name__ == "__main__":
    main()
