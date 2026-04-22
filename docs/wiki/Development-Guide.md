# Development Guide

This page covers the repository layout, coding conventions, development environment, and how to make changes safely.

---

## Repository Layout

```
.
├── .devcontainer/
│   └── devcontainer.json        # VS Code devcontainer config (Python 3.13)
├── .github/
│   ├── copilot-instructions.md  # GitHub Copilot context file
│   ├── steps/                   # GitHub Skills exercise step content
│   └── workflows/               # GitHub Actions workflow files
├── docs/
│   └── wiki/                    # Project wiki documentation (this folder)
├── src/
│   ├── app.py                   # FastAPI application (entry point)
│   ├── README.md                # Short API quickstart guide
│   └── static/
│       ├── index.html           # Web UI markup
│       ├── app.js               # Web UI behaviour
│       └── styles.css           # Web UI styles
├── tests/
│   ├── conftest.py              # Pytest fixtures
│   └── test_activities_api.py  # API integration tests
├── .gitignore
├── LICENSE
├── pytest.ini                   # Pytest configuration
├── README.md                    # Repository readme
└── requirements.txt             # Python dependencies
```

---

## Key Files

| File | Role |
|------|------|
| `src/app.py` | The entire backend: FastAPI `app` instance, in-memory data, all route handlers |
| `src/static/app.js` | All frontend JavaScript (no build step required) |
| `requirements.txt` | Runtime **and** test dependencies |
| `pytest.ini` | Sets `pythonpath = .`, `testpaths = tests`, test discovery patterns |
| `tests/conftest.py` | Shared test fixtures; must be kept in sync with `src/app.py` activities |

---

## Devcontainer

The repository ships with a devcontainer configuration for VS Code:

```json
// .devcontainer/devcontainer.json
{
  "image": "mcr.microsoft.com/devcontainers/python:3.13",
  "forwardPorts": [8000],
  "postCreateCommand": "pip install -r requirements.txt",
  "customizations": {
    "vscode": {
      "extensions": ["ms-python.python", "ms-python.debugpy",
                     "GitHub.copilot-chat", "GitHub.copilot"]
    }
  }
}
```

Open the folder in VS Code and choose **Reopen in Container** to get a ready-to-use Python 3.13 environment with GitHub Copilot pre-installed.

---

## Coding Conventions

| Concern | Convention |
|---------|------------|
| Language version | Python 3.10+ (3.13 in devcontainer) |
| Style | PEP 8 (standard Python style) |
| Comments | Inline comments for non-obvious logic; docstrings on route functions |
| Error handling | Use `fastapi.HTTPException` with appropriate status codes and a `detail` string |
| Route parameters | Path params for resource identity (`activity_name`); query params for data (`email`) |
| Frontend | Vanilla JS, no framework, no build tool |

---

## Making a Backend Change

1. Edit `src/app.py`.
2. The Uvicorn `--reload` flag will restart the server automatically.
3. Check `/docs` to verify the route appears correctly in the OpenAPI spec.
4. Add or update tests in `tests/test_activities_api.py`.
5. Run `pytest -q` to confirm all tests pass.

### Important constraint

The module-level name `app` **must not be renamed** — tests import it as:

```python
from src.app import app as fastapi_app
```

Similarly, the module-level name `activities` must remain accessible as `src.app.activities` for the test fixtures to swap it out correctly.

---

## Making a Frontend Change

1. Edit files in `src/static/`.
2. Hard-refresh the browser (`Ctrl+Shift+R` / `Cmd+Shift+R`) to bypass the browser cache.
3. No build step is required.

---

## Adding a Dependency

1. Install it in your virtual environment: `pip install <package>`.
2. Add it to `requirements.txt` (one package per line, no version pin unless required).
3. Commit both changes together.

---

## GitHub Actions Workflows

The `.github/workflows/` directory contains **GitHub Skills exercise progression** workflows, not general CI. They:

- Check branch naming conventions.
- Post step-by-step instructions as issue comments.
- Enable the next step's workflow once criteria are met.

They are **not** general-purpose test or lint runners. Run `pytest` locally before opening a pull request.
