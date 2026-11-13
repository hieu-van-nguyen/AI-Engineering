# AI Engineering

A personal, hands-on learning repo for becoming an AI engineer: a ~180-day curriculum with daily practice, code exercises, a learning journal, and a library of prompt-engineering examples.

## What's Inside

| Path | Purpose |
| :--- | :--- |
| `m1-foundations/` | Module 1: Python refresher, async programming, HTTP clients (`py_refresh.py`, `async_basics.py`, `fetch_one.py`) |
| `m2-ml-dl/` | Module 2: machine learning and deep learning *(not started)* |
| `m3-rag/` | Module 3: retrieval-augmented generation *(not started)* |
| `m4-agents/` | Module 4: agents and tool use *(not started)* |
| `m5-production/` | Module 5: shipping and operating AI apps *(not started)* |
| `m6-capstone/` | Module 6: capstone project *(not started)* |
| `days/` | Per-day work |
| `journal/` | Daily learning logs (`YYYY-MM-DD.md`), based on `TEMPLATE.md` |
| `notes/progress.md` | Day 1–180 progress tracker |
| `prompt/` | Prompt examples and iterations: app ideation, e-commerce data analysis |
| `anthropic_eg_01.py` / `.js` | Minimal "hello world" calls to the Anthropic Messages API |
| `check_env.py` | Prints which API keys are configured (values are never shown) |

## Getting Started

### Prerequisites
- Python 3.13+ and [uv](https://docs.astral.sh/uv/)
- Node.js (only for the JS example)
- An Anthropic API key, or a local Anthropic-compatible endpoint such as [Ollama](https://ollama.com)

### Setup
```bash
# 1. Install Python dependencies
uv sync

# 2. Create your env file and fill in values
cp .env.example .env

# 3. Check that your keys are picked up
uv run python check_env.py

# 4. (Optional) JS example dependencies
npm install
```

### Configuration (`.env`)
| Variable | Description |
| :--- | :--- |
| `ANTHROPIC_API_KEY` / `ANTHROPIC_AUTH_TOKEN` | Credentials for the Anthropic API or gateway |
| `ANTHROPIC_BASE_URL` | Override the API endpoint (e.g. `http://127.0.0.1:11434` for Ollama) |
| `ANTHROPIC_MODEL` | Model name used by the Python example |
| `OPENAI_*` | Equivalent settings for OpenAI-compatible endpoints |

`.env` is gitignored. Never commit it.

## Running the Examples

```bash
# Anthropic Messages API
uv run python anthropic_eg_01.py
node anthropic_eg_01.js            # note: model is hardcoded in this file

# Module 1 exercises
uv run python m1-foundations/async_basics.py

# Fetch a URL with httpx (defaults to a local server)
python -m http.server 8000         # in a separate terminal
uv run python m1-foundations/fetch_one.py
uv run python m1-foundations/fetch_one.py https://httpbin.org/get
```

### Using a local model with Ollama
To try the examples without an API bill, run a local model and point the base URL at it:
```bash
ollama cp qwen2.5-coder:7b anthropic/claude-4-5-sonnet
# .env: ANTHROPIC_BASE_URL=http://127.0.0.1:11434, ANTHROPIC_API_KEY=ollama
```
See `Claude Desktop Config.txt` for more notes.

## Daily Workflow
1. Work on the day's topic in the relevant `m*/` module.
2. Copy `journal/TEMPLATE.md` to `journal/YYYY-MM-DD.md` and fill it in: time spent, what broke, what you learned, tomorrow's first step.
3. Mark the day `[ v ]` in `notes/progress.md`.

## Prompt Library

`prompt/` holds reusable prompt templates and their iterations:
- `Build_With_AI.txt`: prompts for building AI-powered apps (decision makers, brand builders)
- `prompt_20260426.txt`, `prompt_20260427.txt`: e-commerce analysis and business-performance reviews

Copy a prompt as a starting point and adapt it to your own use case.

## Tooling
- **Type checking:** `uv run mypy <file>`
- **Tests:** `uv run pytest` (none written yet)
- **Notebooks:** `uv run jupyter notebook`
