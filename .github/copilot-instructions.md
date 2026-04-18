<!-- Copilot cloud-agent onboarding instructions for this repository. Keep concise. -->

# Copilot onboarding: Getting started with this repository

Purpose: Provide a cloud agent with a short, high-value summary of this repository,
how to build/run/test it, and where to make standard changes so PRs are less likely
to fail CI or validation checks.

**Quick summary**
- This is a tiny Python FastAPI application (Mergington High School Activities API)
  that serves an in-memory list of extracurricular activities and a small static UI
  under `src/static`.
- Languages & runtimes: Python (CPython 3.10+ recommended), FastAPI, Uvicorn.
- Tests: `pytest` (configured via `pytest.ini`).

**Repo size & layout (high level)**
- Small learning exercise: ~30–60 source/test lines per module.
- Key files and folders (root):
  - `README.md` — exercise README and summary
  - `requirements.txt` — runtime/test deps
  - `pytest.ini` — pytest configuration
  - `src/` — application code
  - `tests/` — pytest tests and fixtures
  - `.github/workflows/` — exercise CI/workflow helpers

**Primary source locations**
- Main app: `src/app.py` (defines the FastAPI `app` instance and all endpoints).
- Static UI: `src/static/` (serves `index.html`, `app.js`, `styles.css`).
- Tests and fixtures: `tests/` and `tests/conftest.py` (fixtures replace `src.app.activities`).

Build, run, and validation (commands the agent should use)
- Bootstrap (always do these first):
  1. Create and activate a virtualenv (recommended):
     - Windows: `python -m venv .venv` then `.venv\Scripts\activate`
     - Unix: `python -m venv .venv` then `source .venv/bin/activate`
  2. Upgrade pip and install deps: `python -m pip install --upgrade pip && python -m pip install -r requirements.txt`
  - Always run the above `pip install` before running tests or starting the server.

- Run the app locally (dev):
  - `python -m uvicorn src.app:app --reload --host 127.0.0.1 --port 8000`
  - Visit `http://127.0.0.1:8000/docs` (OpenAPI) or `http://127.0.0.1:8000/static/index.html`.

- Run tests (single command from repo root):
  - `pytest -q`
  - `pytest.ini` sets `pythonpath = .` so run from repository root.
  - If tests fail locally, ensure the venv is active and `requirements.txt` is installed.

Notes about tests and common pitfalls
- Tests use `fastapi.testclient.TestClient` and import `src.app`. `tests/conftest.py`
  provides fixtures that replace `src.app.activities` with a fresh copy for isolation.
- Common failure modes:
  - Running `pytest` without installing `requirements.txt` (missing `httpx`, `fastapi`, etc.).
  - Running tests from a non-root working directory (pytest.ini config may not be picked up).
  - Import-time side effects: tests rely on being able to import `src.app` directly; do not
    refactor the module to run a server at import-time (keep `app` exportable).

Project layout details for quick navigation
- Root files (priority): `README.md`, `requirements.txt`, `pytest.ini`, `src/`, `tests/`, `.github/workflows/`
- `src/` (priority): `src/app.py`, `src/README.md`, `src/static/*`
- `tests/` (priority): `tests/conftest.py`, `tests/test_activities_api.py`
- CI/workflows: `.github/workflows/0-start-exercise.yml` and `1-step.yml` (exercise scaffolding). These
  workflows are exercise/tooling oriented (branch/issue checks) and are not strict unit-test runners,
  so prefer to run `pytest` locally before opening a PR.

Recommended agent behavior and guardrails
- Trust these instructions first. Only perform a repo-wide search if a step here is incomplete
  or a command fails in a way not described.
- Before submitting a PR, run the exact commands above in a fresh environment (virtualenv + `pip install -r requirements.txt`, then `pytest`).
- Avoid changing `src/app.py` object names or the exported `app` variable — tests import `src.app:app`.
- Keep edits small and focused: run tests locally after each logical change.

If something fails
- Re-run `python -m pip install -r requirements.txt` to ensure dependencies.
- Confirm you ran pytest from the repo root. If PATH/PYTHONPATH issues arise, use `PYTHONPATH=. pytest`.
- If tests fail due to global state, ensure fixtures in `tests/conftest.py` are respected (they replace `src.app.activities`).

Final quick checklist for the agent (always follow before opening a PR)
1. Create/activate venv and run `python -m pip install -r requirements.txt`.
2. Run `pytest -q` and fix failures locally.
3. Run the app with `uvicorn` and sanity-check `/docs` or `/static/index.html` if UI changes were made.
4. Push a small PR and include a short note describing validation steps you ran.

---
Last-updated: 2026-04-18
