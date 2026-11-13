# Dataclass vs. Pydantic model

**In one line:** a `@dataclass` is a convenient way to *hold* data you already trust, while a Pydantic `BaseModel` *checks and converts* data you don't trust yet (user input, JSON, API responses, LLM output) and turns it back into JSON.

Both look almost the same to write:

```python
from dataclasses import dataclass, field
from datetime import date
from typing import Literal
from pydantic import BaseModel

@dataclass
class TicketDC:
    id: int
    title: str
    priority: Literal["low", "medium", "high"]
    tags: list[str] = field(default_factory=list)  # a plain [] default is an error here
    due: date | None = None

class TicketPD(BaseModel):
    id: int
    title: str
    priority: Literal["low", "medium", "high"]
    tags: list[str] = []  # fine: Pydantic copies the default for each instance
    due: date | None = None
```

The difference is what happens at runtime. In a dataclass the type hints are **documentation for you and mypy**; in Pydantic they are **rules that run** every time an object is created.

## Summary

| | `@dataclass` (standard library) | Pydantic `BaseModel` |
|---|---|---|
| Type hints at runtime | Ignored | Enforced |
| Validation | None (add it yourself in `__post_init__`) | Built in, plus `field_validator` / `model_validator` |
| Parsing / conversion | None: `"2"` stays a string | `"2"` → `2`, `"2026-11-13"` → `date` |
| Errors | Whatever goes wrong later | One `ValidationError` listing every problem |
| Unknown fields | `TypeError` | Ignored by default (configurable) |
| To dict | `dataclasses.asdict(obj)` | `obj.model_dump()` |
| To / from JSON | Do it yourself with `json` (fails on `date` etc.) | `model_dump_json()` / `model_validate_json()` |
| JSON Schema | No | `Model.model_json_schema()` |
| Speed / dependencies | Fastest, no install | Slightly slower to create objects, extra package |

## 1. Validation

A dataclass accepts anything:

```python
TicketDC(id="abc", title=123, priority="urgent")
# TicketDC(id='abc', title=123, priority='urgent', tags=[], due=None)  <- no error
```

The bad data gets in silently and breaks something later, far from where it came in.

Pydantic rejects it immediately and reports **every** problem at once:

```python
TicketPD(id="abc", title=123, priority="urgent")
# ValidationError: 3 errors -> int_parsing (id), string_type (title), literal_error (priority)
```

Custom rules go in a `field_validator` (see `m1-foundations/pydantic_basics.py`, where a blank title is rejected). With a dataclass you would write the same checks by hand in `__post_init__` and raise your own errors.

**Watch out:** Pydantic validates on creation, not on assignment. `ticket.id = "zzz"` is accepted unless you set `model_config = ConfigDict(validate_assignment=True)`.

## 2. Parsing (converting input to the right types)

External data almost never arrives with the right Python types: JSON has no `date`, query strings are all text, and so on.

```python
data = {"id": "2", "title": "x", "priority": "low", "due": "2026-11-13"}

TicketDC(**data)  # id='2', due='2026-11-13'                  <- still strings
TicketPD(**data)  # id=2,   due=datetime.date(2026, 11, 13)   <- converted
```

Pydantic's default "lax" mode converts values when the meaning is clear (`"2"` → `2`) and refuses when it isn't (`"abc"` → error). If you want no conversion at all, use strict mode (`ConfigDict(strict=True)` or `Field(strict=True)`).

It can also read raw JSON directly: `TicketPD.model_validate_json('{"id": 1, ...}')`. A dataclass needs `json.loads` first, then manual conversion of each field.

## 3. Serialization (back to dict / JSON)

```python
from dataclasses import asdict
import json

json.dumps(asdict(TicketDC(1, "x", "low", due=date(2026, 11, 13))))
# TypeError: Object of type date is not JSON serializable

TicketPD(id=1, title="x", priority="low", due=date(2026, 11, 13)).model_dump_json()
# '{"id":1,"title":"x","priority":"low","tags":[],"due":"2026-11-13"}'
```

- `model_dump()` → dict with Python objects (`date` stays a `date`).
- `model_dump(mode="json")` → dict with only JSON-safe values (`date` becomes `"2026-11-13"`).
- `model_dump_json()` → JSON string. Round-trips with `model_validate_json()`.
- Options like `exclude=`, `include=`, `exclude_none=True` and `by_alias=True` control the output.

## When to use which

- **Pydantic** at the edges of a program, wherever data comes from outside: API requests and responses, config files, `.env` settings (`pydantic-settings`), and structured output from an LLM. Its JSON Schema output is also what tool-calling and structured-output APIs expect.
- **Dataclass** for internal data that your own code builds and already trusts, when you want something light with no extra dependency.

A common pattern: validate with Pydantic at the boundary, then pass trusted objects around inside.

**Middle ground:** Pydantic can validate a plain dataclass without changing it, via `TypeAdapter(TicketDC).validate_python(data)` (this converts `"2"` → `2` too), or you can use `pydantic.dataclasses.dataclass` to get dataclass syntax with validation.
