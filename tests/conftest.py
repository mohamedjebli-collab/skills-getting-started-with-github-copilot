"""
Pytest configuration and fixtures for the Mergington High School Activities API tests.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app as fastapi_app


@pytest.fixture
def mock_activities():
    """
    Fixture that provides a fresh copy of the activities dictionary for each test.
    This ensures test isolation by preventing state from leaking between tests.
    """
    return {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Competitive basketball team and training",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["alex@mergington.edu"]
        },
        "Tennis Club": {
            "description": "Tennis lessons and practice matches",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 16,
            "participants": ["ryan@mergington.edu", "jessica@mergington.edu"]
        },
        "Art Studio": {
            "description": "Painting, drawing, and mixed media art",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["isabella@mergington.edu"]
        },
        "Music Band": {
            "description": "Learn instruments and perform in the school band",
            "schedule": "Mondays and Fridays, 3:45 PM - 4:45 PM",
            "max_participants": 25,
            "participants": ["noah@mergington.edu", "ava@mergington.edu"]
        },
        "Debate Team": {
            "description": "Compete in debate competitions and develop argumentation skills",
            "schedule": "Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 10,
            "participants": ["grace@mergington.edu"]
        },
        "Science Club": {
            "description": "Explore STEM topics through experiments and projects",
            "schedule": "Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 22,
            "participants": ["lucas@mergington.edu", "mia@mergington.edu"]
        }
    }


@pytest.fixture
def app_with_mock_data(mock_activities):
    """
    Fixture that provides a FastAPI app instance with mocked activities data.
    Replaces the global activities dictionary with test data.
    """
    # Replace the app's activities with mock data for this test
    import src.app
    original_activities = src.app.activities.copy()
    src.app.activities.clear()
    src.app.activities.update(mock_activities)
    
    yield fastapi_app
    
    # Restore original activities after test completes
    src.app.activities.clear()
    src.app.activities.update(original_activities)


@pytest.fixture
def client(app_with_mock_data):
    """
    Fixture that provides a TestClient for making HTTP requests to the FastAPI app.
    Uses the app_with_mock_data fixture to ensure mocked data is available.
    """
    return TestClient(app_with_mock_data)
