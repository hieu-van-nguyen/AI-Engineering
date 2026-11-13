# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
A personal AI Engineering learning repo (a ~180-day curriculum, tracked day by day) plus a collection of prompt-engineering examples. It mixes small Python/JS scripts that call the Anthropic API, learning exercises, and daily notes. There is no application, build step, or test suite yet.

## Repository Structure
- `prompt/`: `.txt` prompt examples and iterations (`Build_With_AI.txt`, `prompt_20260426.txt`, `prompt_20260427.txt` — app ideation, e-commerce analysis).
- `m1-foundations/` … `m6-capstone/`: curriculum modules (foundations, ML/DL, RAG, agents, production, capstone). Only `m1-foundations/` has code so far (`py_refresh.py`, `async_basics.py`, `fetch_one.py`); the others contain only `.gitkeep`.
- `days/`: placeholder for per-day work (`.gitkeep`).
- `journal/`: daily learning logs named `YYYY-MM-DD.md`; copy `journal/TEMPLATE.md` (time spent, what I did, what broke, what I learned, tomorrow's first step).
- `notes/progress.md`: Day 1–180 progress table; mark a day `[ v ]` when done.
- Root scripts: `anthropic_eg_01.py` / `anthropic_eg_01.js` (minimal Messages API example), `check_env.py` (prints which API keys are set).
- `Claude Desktop Config.txt`: scratch notes for pointing Claude at a local Ollama model (`ollama cp ... anthropic/claude-*`, base URL `http://127.0.0.1:11434`).

## Setup & Commands
- Python ≥ 3.13, managed with **uv** (`pyproject.toml`, `uv.lock`, `.venv/`). Install: `uv sync`. Run: `uv run python <file>`.
- Python deps: `anthropic`, `httpx`, `jupyter`, `pydantic`, `pytest`, `python-dotenv`; dev: `mypy`. Type-check with `uv run mypy <file>`; tests (when added) with `uv run pytest`.
- JS (Node, CommonJS): `npm install`, then `node anthropic_eg_01.js`. Deps: `@anthropic-ai/sdk`, `dotenv`. `npm test` is a stub.
- Verify env config: `uv run python check_env.py`.
- `m1-foundations/fetch_one.py` defaults to a local server: run `python -m http.server 8000` in another terminal first, or pass a URL as the first argument.

## Configuration
- Secrets/config live in `.env` (gitignored; `.env.example` is the template): `ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN`, `ANTHROPIC_BASE_URL`, `ANTHROPIC_MODEL`, plus OpenAI equivalents. Never commit `.env`.
- The example scripts read `ANTHROPIC_BASE_URL`/`ANTHROPIC_MODEL` from env, so they can target a local Ollama endpoint or another Anthropic-compatible gateway. Note the JS example hardcodes `model = "qwen2.5-coder:7b"` rather than reading `ANTHROPIC_MODEL`.

## Conventions
- Scripts are small, standalone, and use type hints and docstrings (see `m1-foundations/`).
- Load env with `python-dotenv` (`load_dotenv()`) / `dotenv` in JS.
- Keep a journal entry and update `notes/progress.md` as part of finishing a learning day.
