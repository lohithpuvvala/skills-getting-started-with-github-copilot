"""
Tests for the Mergington High School API endpoints.

Uses the AAA (Arrange-Act-Assert) testing pattern for clear test structure.
"""

import pytest


class TestGetActivities:
    """Tests for GET /activities endpoint."""

    def test_get_activities_returns_all_activities(self, client):
        """Test that GET /activities returns all activities."""
        # Arrange - No special setup needed

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) > 0
        assert "Chess Club" in data

    def test_get_activities_structure(self, client):
        """Test that activities have the correct structure."""
        # Arrange - No special setup needed

        # Act
        response = client.get("/activities")

        # Assert
        data = response.json()
        for activity_name, activity_data in data.items():
            assert "description" in activity_data
            assert "schedule" in activity_data
            assert "max_participants" in activity_data
            assert "participants" in activity_data
            assert isinstance(activity_data["participants"], list)


class TestSignupActivity:
    """Tests for POST /activities/{activity_name}/signup endpoint."""

    def test_signup_success(self, client, sample_activity_name, sample_email):
        """Test successful signup for an activity."""
        # Arrange - Use fixtures for test data

        # Act
        response = client.post(
            f"/activities/{sample_activity_name}/signup",
            params={"email": sample_email}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "signed up" in data["message"].lower()

    def test_signup_duplicate_email(self, client, sample_activity_name, existing_email):
        """Test that duplicate signup is rejected."""
        # Arrange - existing_email is already signed up for Chess Club

        # Act
        response = client.post(
            f"/activities/{sample_activity_name}/signup",
            params={"email": existing_email}
        )

        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"].lower()

    def test_signup_nonexistent_activity(self, client, nonexistent_activity_name, sample_email):
        """Test signup fails for non-existent activity."""
        # Arrange - nonexistent_activity_name is not a valid activity

        # Act
        response = client.post(
            f"/activities/{nonexistent_activity_name}/signup",
            params={"email": sample_email}
        )

        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_signup_verifies_participant_added(self, client, sample_activity_name, sample_email):
        """Test that participant is actually added to the activity."""
        # Arrange - Clean state from reset_activities fixture

        # Act
        client.post(
            f"/activities/{sample_activity_name}/signup",
            params={"email": sample_email}
        )

        # Assert - Check that the participant was added
        response = client.get("/activities")
        activities = response.json()
        assert sample_email in activities[sample_activity_name]["participants"]


class TestRemoveParticipant:
    """Tests for DELETE /activities/{activity_name}/participants/{email} endpoint."""

    def test_remove_existing_participant(self, client, sample_activity_name, existing_email):
        """Test successful removal of a participant."""
        # Arrange - existing_email is already signed up

        # Act
        response = client.delete(
            f"/activities/{sample_activity_name}/participants/{existing_email}"
        )

        # Assert
        assert response.status_code == 200
        assert "removed" in response.json()["message"].lower()

    def test_remove_nonexistent_participant(self, client, sample_activity_name, sample_email):
        """Test removal fails when participant not in activity."""
        # Arrange - sample_email is not signed up for Chess Club

        # Act
        response = client.delete(
            f"/activities/{sample_activity_name}/participants/{sample_email}"
        )

        # Assert
        assert response.status_code == 404
        assert "not signed up" in response.json()["detail"].lower()

    def test_remove_from_nonexistent_activity(self, client, nonexistent_activity_name, sample_email):
        """Test removal fails for non-existent activity."""
        # Arrange - nonexistent_activity_name is not a valid activity

        # Act
        response = client.delete(
            f"/activities/{nonexistent_activity_name}/participants/{sample_email}"
        )

        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_remove_verifies_participant_removed(self, client, sample_activity_name, existing_email):
        """Test that participant is actually removed from the activity."""
        # Arrange - existing_email is signed up for Chess Club

        # Act
        client.delete(
            f"/activities/{sample_activity_name}/participants/{existing_email}"
        )

        # Assert - Check that the participant was removed
        response = client.get("/activities")
        activities = response.json()
        assert existing_email not in activities[sample_activity_name]["participants"]


class TestRootEndpoint:
    """Tests for the root endpoint."""

    def test_root_redirect(self, client):
        """Test that root endpoint redirects to static files."""
        # Arrange - No special setup needed

        # Act
        response = client.get("/", follow_redirects=False)

        # Assert
        assert response.status_code in [307, 308]  # Redirect status codes
        assert response.headers.get("location") == "/static/index.html"