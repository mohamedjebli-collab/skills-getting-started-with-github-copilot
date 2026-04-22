# Mergington High School Activities — Wiki

Welcome to the project wiki for the **Mergington High School Activities** application.  
This is a small, self-contained Python web application that lets students browse and sign up for extracurricular activities.

---

## Table of Contents

| Page | Description |
|------|-------------|
| [Getting Started](Getting-Started.md) | Install dependencies, run the app, and open the UI |
| [API Reference](API-Reference.md) | Endpoint details, parameters, request/response examples, and error codes |
| [Data Model](Data-Model.md) | Activity object schema and in-memory storage design |
| [Frontend Guide](Frontend-Guide.md) | Static UI structure, JavaScript flow, and CSS conventions |
| [Development Guide](Development-Guide.md) | Repository layout, coding conventions, and devcontainer setup |
| [Testing Guide](Testing-Guide.md) | Running tests, fixture design, and writing new tests |

---

## Project Overview

**Mergington High School Activities** is a lightweight FastAPI backend that exposes a REST API for:

- Viewing all available extracurricular activities
- Signing students up for an activity
- Unregistering students from an activity

A static HTML/CSS/JS frontend is served directly by the same FastAPI server, so the whole application runs as a single process with no external database.

### Key facts

| Item | Detail |
|------|--------|
| Language | Python 3.10+ (devcontainer: Python 3.13) |
| Web framework | [FastAPI](https://fastapi.tiangolo.com/) |
| ASGI server | [Uvicorn](https://www.uvicorn.org/) |
| Frontend | Vanilla HTML / CSS / JavaScript (no build step) |
| Storage | In-memory Python dictionary (resets on restart) |
| Test runner | [Pytest](https://docs.pytest.org/) + FastAPI `TestClient` |

### Architecture at a glance

```
Browser
  │
  ▼
Uvicorn (ASGI server)
  │
  ▼
FastAPI app  (src/app.py)
  ├─ GET  /                    → redirect to /static/index.html
  ├─ GET  /activities          → return all activities (JSON)
  ├─ POST /activities/{name}/signup   → register a student
  ├─ DELETE /activities/{name}/signup → unregister a student
  └─ /static/*                 → serve HTML, CSS, JS (src/static/)
```
