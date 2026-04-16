import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


class TestActivitiesEndpoint:
    def test_get_activities_returns_dict(self):
        """Test that /activities endpoint returns activities dictionary"""
        response = client.get("/activities")
        assert response.status_code == 200
        assert isinstance(response.json(), dict)
        assert "Chess Club" in response.json()

    def test_get_activities_has_required_fields(self):
        """Test that activities have required fields"""
        response = client.get("/activities")
        activities = response.json()
        chess_club = activities["Chess Club"]
        assert "description" in chess_club
        assert "schedule" in chess_club
        assert "max_participants" in chess_club
        assert "participants" in chess_club


class TestSignupEndpoint:
    def test_signup_for_activity_success(self):
        """Test successful signup for an activity"""
        response = client.post(
            "/activities/Soccer Team/signup",
            params={"email": "test@mergington.edu"}
        )
        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]

    def test_signup_duplicate_email(self):
        """Test that duplicate signup is rejected"""
        email = "duplicate@mergington.edu"
        # First signup
        client.post("/activities/Soccer Team/signup", params={"email": email})
        # Second signup should fail
        response = client.post(
            "/activities/Soccer Team/signup",
            params={"email": email}
        )
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]

    def test_signup_nonexistent_activity(self):
        """Test signup for nonexistent activity"""
        response = client.post(
            "/activities/Fake Activity/signup",
            params={"email": "test@mergington.edu"}
        )
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]


class TestUnregisterEndpoint:
    def test_unregister_success(self):
        """Test successful unregister from activity"""
        email = "unregister@mergington.edu"
        # Sign up first
        client.post("/activities/Programming Class/signup",
                    params={"email": email})
        # Now unregister
        response = client.delete(
            "/activities/Programming Class/unregister",
            params={"email": email}
        )
        assert response.status_code == 200
        assert "Unregistered" in response.json()["message"]

    def test_unregister_not_signed_up(self):
        """Test unregister returns error if not signed up"""
        response = client.delete(
            "/activities/Chess Club/unregister",
            params={"email": "notregistered@mergington.edu"}
        )
        assert response.status_code == 400
        assert "not registered" in response.json()["detail"]

    def test_unregister_nonexistent_activity(self):
        """Test unregister from nonexistent activity"""
        response = client.delete(
            "/activities/Fake Activity/unregister",
            params={"email": "test@mergington.edu"}
        )
        assert response.status_code == 404
