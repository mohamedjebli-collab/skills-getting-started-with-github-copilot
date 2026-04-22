# Testing Guide

This page explains how to run the test suite, how the fixtures work, and how to write new tests.

---

## Running the Tests

From the **repository root** (where `pytest.ini` lives):

```bash
pytest -q
```

Useful flags:

| Flag | Description |
|------|-------------|
| `-q` | Quiet output — shows dots for passes, letters for failures |
| `-v` | Verbose output — shows each test name |
| `-k "signup"` | Run only tests whose name contains `signup` |
| `--tb=short` | Shorter tracebacks on failure |
| `pytest tests/test_activities_api.py::TestSignupForActivity` | Run a single class |

> The `pytest.ini` sets `pythonpath = .` so the test files can `import src.app` without any path manipulation.

---

## Test File Layout

```
tests/
├── conftest.py              # Fixtures shared across all test files
└── test_activities_api.py  # All API tests
```

### `test_activities_api.py` — Test Classes

| Class | Endpoint covered |
|-------|-----------------|
| `TestGetActivities` | `GET /activities` |
| `TestSignupForActivity` | `POST /activities/{name}/signup` |
| `TestUnregisterFromActivity` | `DELETE /activities/{name}/signup` |
| `TestEdgeCases` | Cross-endpoint workflows |

Tests follow the **Arrange-Act-Assert (AAA)** pattern with inline comments labelling each section.

---

## Fixtures (conftest.py)

### `mock_activities`

Returns a **fresh copy** of the nine default activities as a plain Python dictionary.  
Used to reset state for each test.

```python
@pytest.fixture
def mock_activities():
    return { "Chess Club": { ... }, ... }
```

### `app_with_mock_data`

Replaces the global `src.app.activities` dictionary with the mock data **before** the test, then restores the original data **after** the test (teardown via `yield`).

```python
@pytest.fixture
def app_with_mock_data(mock_activities):
    import src.app
    original = src.app.activities.copy()
    src.app.activities.clear()
    src.app.activities.update(mock_activities)
    yield fastapi_app               # test runs here
    src.app.activities.clear()
    src.app.activities.update(original)
```

This ensures that mutations made during one test (e.g. adding a participant) never bleed into another test.

### `client`

Wraps `app_with_mock_data` in a FastAPI `TestClient`, ready for HTTP requests.

```python
@pytest.fixture
def client(app_with_mock_data):
    return TestClient(app_with_mock_data)
```

**In your tests, always use the `client` fixture.** You get both the HTTP client and isolated data automatically.

---

## Writing a New Test

### Minimal example

```python
class TestGetActivities:
    def test_get_activities_returns_all_activities(self, client):
        # Arrange (implicit — fixture provides data)

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        assert len(response.json()) == 9
```

### Key rules

1. **Always accept `client` as a parameter** — this pulls in `app_with_mock_data` automatically and gives you an isolated state.
2. Accept `mock_activities` as well when you need to **directly mutate** pre-existing data before the request (e.g., prefilling a participant).
3. Use **AAA comments** (`# Arrange`, `# Act`, `# Assert`) consistent with the existing tests.
4. Place tests that cover a new endpoint in a new class named `TestYourFeatureName`.
5. Test both **success** and **error** paths.

### Example — testing a new endpoint

```python
class TestMyNewEndpoint:
    def test_success_case(self, client):
        # Arrange
        payload = { ... }

        # Act
        response = client.post("/my-endpoint", json=payload)

        # Assert
        assert response.status_code == 200
        assert response.json()["key"] == "expected_value"

    def test_error_case_not_found(self, client):
        # Arrange
        invalid_name = "Does Not Exist"

        # Act
        response = client.get(f"/my-endpoint/{invalid_name}")

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Not found"
```

---

## Test Isolation Notes

- The `mock_activities` fixture provides the same nine activities that the real app starts with.
- Because `app_with_mock_data` swaps and restores the global `activities` dict, tests that modify participants (signup / unregister) do **not** affect other tests.
- If you add or rename activities in `src/app.py`, update the `mock_activities` fixture in `tests/conftest.py` and adjust any count assertions (e.g., `assert len(activities) == 9`).

---

## Continuous Integration

There is no dedicated CI test workflow in this repository (the GitHub Actions workflows are for the GitHub Skills exercise, not for running `pytest`). Run tests locally before opening a pull request:

```bash
pip install -r requirements.txt
pytest -q
```
