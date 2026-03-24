import pytest


def test_remove_participant_successful(client, activities_backup):
    """Test successfully removing a participant from an activity"""
    # Arrange: Participant is signed up for Tennis Club
    activity_name = "Tennis Club"
    participant_email = "james@mergington.edu"
    
    # Act: Send DELETE request to remove participant
    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": participant_email}
    )
    
    # Assert: Verify removal was successful
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert participant_email in data["message"]
    assert activity_name in data["message"]


def test_remove_participant_not_signed_up(client, activities_backup):
    """Test that removing a student not signed up returns error"""
    # Arrange: Student not signed up for Debate Team
    activity_name = "Debate Team"
    non_participant_email = "notasignedupstudent@mergington.edu"
    
    # Act: Try to remove student who is not signed up
    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": non_participant_email}
    )
    
    # Assert: Verify error response
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "not signed up" in data["detail"]


def test_remove_activity_not_found(client, activities_backup):
    """Test that removing from non-existent activity returns error"""
    # Arrange: Non-existent activity
    activity_name = "Nonexistent Activity"
    participant_email = "student@mergington.edu"
    
    # Act: Try to remove participant from activity that doesn't exist
    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": participant_email}
    )
    
    # Assert: Verify activity not found error
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"]


def test_remove_actually_removes_participant(client, activities_backup):
    """Test that delete actually removes participant from the activity"""
    # Arrange: Get initial participant count
    activity_name = "Art Studio"
    participant_email = "grace@mergington.edu"
    
    response_before = client.get("/activities")
    initial_participants = len(response_before.json()[activity_name]["participants"])
    assert participant_email in response_before.json()[activity_name]["participants"]
    
    # Act: Remove the participant
    client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": participant_email}
    )
    
    # Assert: Verify participant was removed
    response_after = client.get("/activities")
    activity_data = response_after.json()[activity_name]
    assert participant_email not in activity_data["participants"]
    assert len(activity_data["participants"]) == initial_participants - 1
