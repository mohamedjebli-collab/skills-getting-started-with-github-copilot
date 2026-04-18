"""
Integration and unit tests for the Mergington High School Activities API.
Tests follow the Arrange-Act-Assert (AAA) pattern for clarity and maintainability.
"""

import pytest


class TestGetActivities:
    """Tests for the GET /activities endpoint."""

    def test_get_activities_returns_all_activities(self, client):
        """
        Test that GET /activities returns all activities with correct data structure.
        
        Arrange: Client is ready (from fixture)
        Act: Make GET request to /activities
        Assert: Response status is 200 and contains all 9 activities
        """
        # Arrange (implicit from fixture)
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        activities = response.json()
        assert len(activities) == 9
        assert "Chess Club" in activities
        assert "Programming Class" in activities
        assert "Gym Class" in activities

    def test_get_activities_returns_correct_structure(self, client):
        """
        Test that each activity contains required fields: description, schedule, 
        max_participants, and participants.
        
        Arrange: Client is ready
        Act: Make GET request to /activities
        Assert: Each activity has required fields with correct types
        """
        # Arrange
        expected_fields = {"description", "schedule", "max_participants", "participants"}
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        for activity_name, activity_data in activities.items():
            assert set(activity_data.keys()) == expected_fields
            assert isinstance(activity_data["description"], str)
            assert isinstance(activity_data["schedule"], str)
            assert isinstance(activity_data["max_participants"], int)
            assert isinstance(activity_data["participants"], list)

    def test_get_activities_returns_correct_participants(self, client):
        """
        Test that GET /activities returns the correct participants for each activity.
        
        Arrange: Expected participants for specific activities
        Act: Make GET request to /activities
        Assert: Participants list matches expected data
        """
        # Arrange
        expected_chess_participants = ["michael@mergington.edu", "daniel@mergington.edu"]
        expected_programming_participants = ["emma@mergington.edu", "sophia@mergington.edu"]
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert activities["Chess Club"]["participants"] == expected_chess_participants
        assert activities["Programming Class"]["participants"] == expected_programming_participants


class TestSignupForActivity:
    """Tests for the POST /activities/{activity_name}/signup endpoint."""

    def test_signup_success_adds_student_to_activity(self, client, mock_activities):
        """
        Test that a student can successfully sign up for an activity.
        
        Arrange: Select a student email and an activity with available spots
        Act: POST to /activities/{activity}/signup with email parameter
        Assert: Response status is 200, message contains success text, student appears in participants
        """
        # Arrange
        new_student = "newstudent@mergington.edu"
        activity_name = "Chess Club"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": new_student}
        )
        
        # Assert
        assert response.status_code == 200
        result = response.json()
        assert "Signed up" in result["message"]
        assert new_student in result["message"]
        
        # Verify student was added to participants
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert new_student in activities[activity_name]["participants"]

    def test_signup_error_activity_not_found(self, client):
        """
        Test that signing up for a non-existent activity returns 404.
        
        Arrange: Select a non-existent activity name and valid email
        Act: POST to /activities/{invalid_activity}/signup
        Assert: Response status is 404 with "Activity not found" detail
        """
        # Arrange
        email = "student@mergington.edu"
        invalid_activity = "Nonexistent Club"
        
        # Act
        response = client.post(
            f"/activities/{invalid_activity}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"

    def test_signup_error_student_already_signed_up(self, client):
        """
        Test that a student already signed up for an activity gets 400 error.
        
        Arrange: Select an email that is already in an activity's participants
        Act: POST /activities/{activity}/signup with existing participant email
        Assert: Response status is 400 with "already signed up" message
        """
        # Arrange
        activity_name = "Chess Club"
        existing_student = "michael@mergington.edu"  # Already in Chess Club
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": existing_student}
        )
        
        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Student already signed up for this activity"

    def test_signup_success_with_url_encoded_activity_name(self, client):
        """
        Test that signup works with URL-encoded activity names containing spaces.
        
        Arrange: Activity name "Programming Class" (contains space requiring encoding)
        Act: POST /activities/Programming%20Class/signup with URL-encoded name
        Assert: Response status is 200 and student is added
        """
        # Arrange
        new_student = "newstudent2@mergington.edu"
        activity_name = "Programming Class"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": new_student}
        )
        
        # Assert
        assert response.status_code == 200
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert new_student in activities[activity_name]["participants"]

    def test_signup_success_multiple_students_same_activity(self, client):
        """
        Test that multiple different students can sign up for the same activity.
        
        Arrange: Two new student emails and one activity
        Act: POST for first student, then POST for second student
        Assert: Both students appear in the activity's participants
        """
        # Arrange
        student1 = "student1@mergington.edu"
        student2 = "student2@mergington.edu"
        activity_name = "Art Studio"
        
        # Act - Sign up student 1
        response1 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": student1}
        )
        assert response1.status_code == 200
        
        # Act - Sign up student 2
        response2 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": student2}
        )
        assert response2.status_code == 200
        
        # Assert
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert student1 in activities[activity_name]["participants"]
        assert student2 in activities[activity_name]["participants"]


class TestUnregisterFromActivity:
    """Tests for the DELETE /activities/{activity_name}/signup endpoint."""

    def test_unregister_success_removes_student_from_activity(self, client):
        """
        Test that a student can successfully unregister from an activity.
        
        Arrange: Select a student email that is already in an activity
        Act: DELETE /activities/{activity}/signup with student email
        Assert: Response status is 200, student no longer in participants
        """
        # Arrange
        activity_name = "Chess Club"
        student_to_remove = "michael@mergington.edu"  # Already in Chess Club
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": student_to_remove}
        )
        
        # Assert
        assert response.status_code == 200
        result = response.json()
        assert "Unregistered" in result["message"]
        assert student_to_remove in result["message"]
        
        # Verify student was removed
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert student_to_remove not in activities[activity_name]["participants"]

    def test_unregister_error_activity_not_found(self, client):
        """
        Test that unregistering from a non-existent activity returns 404.
        
        Arrange: Select a non-existent activity name and valid email
        Act: DELETE /activities/{invalid_activity}/signup
        Assert: Response status is 404 with "Activity not found" detail
        """
        # Arrange
        email = "student@mergington.edu"
        invalid_activity = "Nonexistent Club"
        
        # Act
        response = client.delete(
            f"/activities/{invalid_activity}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"

    def test_unregister_error_student_not_in_activity(self, client):
        """
        Test that unregistering a student not in an activity returns 404.
        
        Arrange: Select an email NOT in the activity's participants
        Act: DELETE /activities/{activity}/signup with non-participating email
        Assert: Response status is 404 with "not signed up" message
        """
        # Arrange
        activity_name = "Chess Club"
        student_not_in_activity = "notinactivity@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": student_not_in_activity}
        )
        
        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Student is not signed up for this activity"

    def test_unregister_removes_only_specified_student(self, client):
        """
        Test that unregistering one student doesn't affect other participants.
        
        Arrange: An activity with 2+ students, select one to remove
        Act: DELETE for one student
        Assert: That student removed, but others remain in participants
        """
        # Arrange
        activity_name = "Programming Class"
        student_to_remove = "emma@mergington.edu"
        other_student = "sophia@mergington.edu"  # Also in Programming Class
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": student_to_remove}
        )
        assert response.status_code == 200
        
        # Assert
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert student_to_remove not in activities[activity_name]["participants"]
        assert other_student in activities[activity_name]["participants"]

    def test_unregister_with_url_encoded_activity_name(self, client):
        """
        Test that unregister works with URL-encoded activity names containing spaces.
        
        Arrange: Activity with space in name and student to remove
        Act: DELETE /activities/{url_encoded_activity}/signup
        Assert: Response status is 200 and student is removed
        """
        # Arrange
        activity_name = "Basketball Team"
        student_to_remove = "alex@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": student_to_remove}
        )
        
        # Assert
        assert response.status_code == 200
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert student_to_remove not in activities[activity_name]["participants"]


class TestEdgeCases:
    """Tests for edge cases and special scenarios."""

    def test_signup_and_unregister_same_student_same_session(self, client):
        """
        Test a complete workflow: sign up, then unregister in same test session.
        
        Arrange: New student email and activity
        Act: POST signup, then DELETE unregister
        Assert: Student appears then disappears from participants
        """
        # Arrange
        student = "workflow@mergington.edu"
        activity_name = "Music Band"
        
        # Act - Sign up
        signup_response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": student}
        )
        assert signup_response.status_code == 200
        
        # Verify student was added
        activities_check1 = client.get("/activities").json()
        assert student in activities_check1[activity_name]["participants"]
        
        # Act - Unregister
        unregister_response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": student}
        )
        assert unregister_response.status_code == 200
        
        # Assert - Verify student was removed
        activities_check2 = client.get("/activities").json()
        assert student not in activities_check2[activity_name]["participants"]

    def test_get_activities_data_consistency(self, client):
        """
        Test that GET /activities returns consistent data across multiple calls.
        
        Arrange: Make multiple GET requests
        Act: Call GET /activities three times
        Assert: All responses are identical (data hasn't changed)
        """
        # Arrange & Act
        response1 = client.get("/activities").json()
        response2 = client.get("/activities").json()
        response3 = client.get("/activities").json()
        
        # Assert
        assert response1 == response2 == response3

    def test_signup_then_list_shows_all_participants(self, client):
        """
        Test that after signup, GET /activities shows updated participant count.
        
        Arrange: Activity with known initial participant count
        Act: Sign up new student, then GET /activities
        Assert: Participant count increased by 1
        """
        # Arrange
        activity_name = "Science Club"
        new_student = "newscientist@mergington.edu"
        
        # Get initial participant count
        initial_activities = client.get("/activities").json()
        initial_count = len(initial_activities[activity_name]["participants"])
        
        # Act - Sign up
        signup_response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": new_student}
        )
        assert signup_response.status_code == 200
        
        # Act - Get activities again
        updated_activities = client.get("/activities").json()
        updated_count = len(updated_activities[activity_name]["participants"])
        
        # Assert
        assert updated_count == initial_count + 1
        assert new_student in updated_activities[activity_name]["participants"]
