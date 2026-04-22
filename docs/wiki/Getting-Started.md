# Getting Started

This page walks you through setting up and running the **Mergington High School Activities** application locally.

---

## Prerequisites

| Requirement | Version |
|-------------|---------|
| Python | 3.10 or later (3.13 recommended) |
| pip | latest |
| Git | any recent version |

> **Devcontainer users**: Open the repository in VS Code with the Dev Containers extension. The container already has Python 3.13 and will run `pip install -r requirements.txt` automatically.

---

## 1 — Clone the repository

```bash
git clone https://github.com/mohamedjebli-collab/skills-getting-started-with-github-copilot.git
cd skills-getting-started-with-github-copilot
```

---

## 2 — Create and activate a virtual environment

**macOS / Linux**
```bash
python -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell)**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

---

## 3 — Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

The `requirements.txt` includes:

| Package | Purpose |
|---------|---------|
| `fastapi` | Web framework |
| `uvicorn` | ASGI server |
| `httpx` | HTTP client (used by FastAPI `TestClient`) |
| `watchfiles` | File-watching for `--reload` mode |
| `pytest` | Test runner |

---

## 4 — Run the application

```bash
python -m uvicorn src.app:app --reload --host 127.0.0.1 --port 8000
```

The server starts on **http://127.0.0.1:8000**.

| URL | Description |
|-----|-------------|
| http://127.0.0.1:8000 | Redirects to the web UI |
| http://127.0.0.1:8000/static/index.html | Student-facing web UI |
| http://127.0.0.1:8000/activities | Raw JSON activity list |
| http://127.0.0.1:8000/docs | Interactive OpenAPI (Swagger) docs |
| http://127.0.0.1:8000/redoc | ReDoc API docs |

---

## 5 — Run the tests

```bash
pytest -q
```

Run from the **repository root** so that `pytest.ini` is picked up (it sets `pythonpath = .`).

All tests should pass. See [Testing Guide](Testing-Guide.md) for details.

---

## Stopping the server

Press `Ctrl+C` in the terminal running Uvicorn.

---

## Notes

- All data is stored **in memory**. Restarting the server resets the participant lists to their defaults.
- The `--reload` flag watches for file changes and restarts the server automatically during development.
