# Data Model

This page describes how the application stores and manages data.

---

## Storage Strategy

The application uses a **plain Python dictionary** stored in module-level memory inside `src/app.py`.

```python
# src/app.py
activities = { ... }   # keyed by activity name (string)
```

There is no database, no file system persistence, and no caching layer.  
All data is **reset to its initial state whenever the server process restarts**.

---

## Activity Record

Each entry in the `activities` dictionary represents one extracurricular activity.

### Key

The dictionary key is the **activity name** (a plain Python string), for example `"Chess Club"`.  
The name is used directly as the `{activity_name}` path parameter in the API.

### Value

Each activity is a nested dictionary with the following fields:

| Field | Python type | Description |
|-------|-------------|-------------|
| `description` | `str` | A one-sentence description of the activity |
| `schedule` | `str` | Human-readable meeting schedule (e.g., `"Fridays, 3:30 PM - 5:00 PM"`) |
| `max_participants` | `int` | Maximum number of participants allowed to sign up |
| `participants` | `list[str]` | Ordered list of student email addresses who are registered |

### Example

```python
"Chess Club": {
    "description": "Learn strategies and compete in chess tournaments",
    "schedule": "Fridays, 3:30 PM - 5:00 PM",
    "max_participants": 12,
    "participants": [
        "michael@mergington.edu",
        "daniel@mergington.edu"
    ]
}
```

---

## Student Identity

Students are identified solely by their **email address** (a string).  
There is no separate `Student` object or table; the email is used directly as an entry in each activity's `participants` list.

### Constraints enforced by the API

| Rule | Enforcement |
|------|-------------|
| A student cannot sign up for the same activity twice | `POST /signup` returns `400` if email already in `participants` |
| A student must be signed up before they can be removed | `DELETE /signup` returns `404` if email not in `participants` |
| The activity must exist | Both endpoints return `404` if `activity_name` not in `activities` |

> **Note:** There is currently no enforcement of `max_participants` at the API level — the field is informational only and displayed in the UI.

---

## Concurrency Considerations

Because FastAPI with Uvicorn in default (single-worker) mode runs in a single process, there are no concurrency issues in typical development use. If deployed with multiple workers or processes, the in-memory store would not be shared and each worker would have independent state. For a production use-case, the in-memory dictionary should be replaced with a persistent database.

---

## Modifying the Initial Data

To change the default activities that load at startup, edit the `activities` dictionary at the top of `src/app.py`:

```python
# src/app.py  (lines 23-78)
activities = {
    "My New Activity": {
        "description": "...",
        "schedule": "...",
        "max_participants": 10,
        "participants": []
    },
    ...
}
```

Remember to update `tests/conftest.py` → `mock_activities` fixture to keep the test data consistent if you change the number or names of activities.
