import pytest


def test_signup_successful(client, activities_backup):
    """Test successfully signing up a new student for an activity"""
    # Arrange: Prepare test data
    activity_name = "Chess Club"
    new_email = "newstudent@mergington.edu"
    
    # Act: Send POST request to signup
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": new_email}
    )
    
    # Assert: Verify signup was successful
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert new_email in data["message"]
    assert activity_name in data["message"]


def test_signup_student_already_exists(client, activities_backup):
    """Test that signing up a student who is already signed up returns error"""
    # Arrange: Student already signed up for Chess Club
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"
    
    # Act: Try to sign up the same student again
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": existing_email}
    )
    
    # Assert: Verify error response
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "already signed up" in data["detail"]


def test_signup_activity_not_found(client, activities_backup):
    """Test that signing up for non-existent activity returns error"""
    # Arrange: Non-existent activity
    activity_name = "Nonexistent Activity"
    new_email = "student@mergington.edu"
    
    # Act: Try to signup for activity that doesn't exist
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": new_email}
    )
    
    # Assert: Verify activity not found error
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"]


def test_signup_adds_participant_to_activity(client, activities_backup):
    """Test that signup actually adds participant to the activity"""
    # Arrange: Get initial participant count
    activity_name = "Programming Class"
    new_email = "testuser@mergington.edu"
    
    response_before = client.get("/activities")
    initial_participants = len(response_before.json()[activity_name]["participants"])
    
    # Act: Sign up the student
    client.post(
        f"/activities/{activity_name}/signup",
        params={"email": new_email}
    )
    
    # Assert: Verify participant was added
    response_after = client.get("/activities")
    activity_data = response_after.json()[activity_name]
    assert new_email in activity_data["participants"]
    assert len(activity_data["participants"]) == initial_participants + 1
