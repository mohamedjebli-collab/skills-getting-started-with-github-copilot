import pytest
from fastapi.testclient import TestClient
from copy import deepcopy
from src.app import app, activities


@pytest.fixture
def client():
    """
    Fixture providing a TestClient for making HTTP requests to the FastAPI app.
    """
    return TestClient(app)


@pytest.fixture
def activities_backup():
    """
    Fixture that backs up the activities dict before each test and restores it after.
    This ensures test isolation by preventing state mutations from affecting other tests.
    """
    original_state = deepcopy(activities)
    yield
    activities.clear()
    activities.update(original_state)
