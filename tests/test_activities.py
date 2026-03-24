import pytest


def test_get_all_activities(client, activities_backup):
    """Test retrieving all activities"""
    # Arrange: Test client is ready
    
    # Act: Send GET request to /activities
    response = client.get("/activities")
    
    # Assert: Verify response status and content
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data


def test_activities_response_structure(client, activities_backup):
    """Test that each activity has the expected structure"""
    # Arrange: Test client is ready
    
    # Act: Send GET request to /activities
    response = client.get("/activities")
    
    # Assert: Verify response structure
    assert response.status_code == 200
    activities = response.json()
    
    for activity_name, activity_data in activities.items():
        assert "description" in activity_data
        assert "schedule" in activity_data
        assert "max_participants" in activity_data
        assert "participants" in activity_data
        assert isinstance(activity_data["participants"], list)


def test_activities_not_empty(client, activities_backup):
    """Test that activities list contains expected number of activities"""
    # Arrange: Test client is ready
    
    # Act: Send GET request to /activities
    response = client.get("/activities")
    
    # Assert: Verify we have multiple activities
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
