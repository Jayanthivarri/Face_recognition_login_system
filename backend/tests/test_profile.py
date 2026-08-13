"""
Profile API Tests

Tests for user profile and list endpoints
"""

import pytest
from fastapi import status

from app.models.user import User


class TestProfile:
    """Tests for profile endpoint"""

    def test_get_profile_success(self, client, sample_user_data, test_db):
        """Test successfully retrieving user profile"""
        # Register user
        reg_response = client.post("/api/register", json=sample_user_data)
        assert reg_response.status_code == status.HTTP_201_CREATED
        user_id = reg_response.json()["data"]["id"]
        
        # Get profile
        response = client.get(f"/api/profile/{user_id}")
        
        assert response.status_code == status.HTTP_200_OK
        
        body = response.json()
        assert body["success"] is True
        assert "data" in body
        
        data = body["data"]
        assert data["id"] == user_id
        assert data["first_name"] == sample_user_data["first_name"]
        assert data["last_name"] == sample_user_data["last_name"]
        assert data["email"] == sample_user_data["email"]
        assert data["age"] == sample_user_data["age"]
        
        # Face embedding should NOT be included
        assert "face_embedding" not in data

    def test_get_profile_not_found(self, client):
        """Test retrieving profile for non-existent user"""
        response = client.get("/api/profile/999999")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        
        body = response.json()
        assert body["success"] is False
        assert "error_code" in body

    def test_get_profile_includes_created_at(self, client, sample_user_data):
        """Test that profile includes created_at timestamp"""
        # Register user
        reg_response = client.post("/api/register", json=sample_user_data)
        user_id = reg_response.json()["data"]["id"]
        
        # Get profile
        response = client.get(f"/api/profile/{user_id}")
        
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()["data"]
        assert "created_at" in data
        assert data["created_at"] is not None

    def test_get_profile_no_embedding(self, client, sample_user_data):
        """Test that profile response does not include face embedding"""
        # Register user
        reg_response = client.post("/api/register", json=sample_user_data)
        user_id = reg_response.json()["data"]["id"]
        
        # Get profile
        response = client.get(f"/api/profile/{user_id}")
        
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()["data"]
        # Explicitly check embedding is not present
        assert "face_embedding" not in data

    def test_get_profile_multiple_users(self, client):
        """Test retrieving profiles for multiple users"""
        user1_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "age": 30,
            "face_embedding": [0.1] * 128
        }
        
        user2_data = {
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane@example.com",
            "age": 28,
            "face_embedding": [0.2] * 128
        }
        
        response1 = client.post("/api/register", json=user1_data)
        response2 = client.post("/api/register", json=user2_data)
        
        user1_id = response1.json()["data"]["id"]
        user2_id = response2.json()["data"]["id"]
        
        # Get both profiles
        profile1 = client.get(f"/api/profile/{user1_id}")
        profile2 = client.get(f"/api/profile/{user2_id}")
        
        assert profile1.status_code == status.HTTP_200_OK
        assert profile2.status_code == status.HTTP_200_OK
        
        # Verify different data
        data1 = profile1.json()["data"]
        data2 = profile2.json()["data"]
        
        assert data1["first_name"] != data2["first_name"]
        assert data1["email"] != data2["email"]

    def test_get_profile_response_structure(self, client, sample_user_data):
        """Test profile response structure"""
        # Register user
        reg_response = client.post("/api/register", json=sample_user_data)
        user_id = reg_response.json()["data"]["id"]
        
        # Get profile
        response = client.get(f"/api/profile/{user_id}")
        
        body = response.json()
        
        # Check top-level structure
        assert "success" in body
        assert "message" in body
        assert "data" in body
        
        # Check data structure
        data = body["data"]
        required_fields = ["id", "first_name", "last_name", "email", "age", "created_at"]
        for field in required_fields:
            assert field in data


class TestListUsers:
    """Tests for list users endpoint"""

    def test_list_users_empty(self, client):
        """Test listing users when no users registered"""
        response = client.get("/api/users")
        
        assert response.status_code == status.HTTP_200_OK
        
        body = response.json()
        assert body["success"] is True
        assert "data" in body
        
        # Should be empty list
        assert isinstance(body["data"], list)
        assert len(body["data"]) == 0

    def test_list_users_single_user(self, client, sample_user_data):
        """Test listing users with one registered user"""
        # Register user
        reg_response = client.post("/api/register", json=sample_user_data)
        assert reg_response.status_code == status.HTTP_201_CREATED
        
        # List users
        response = client.get("/api/users")
        
        assert response.status_code == status.HTTP_200_OK
        
        body = response.json()
        assert body["success"] is True
        
        data = body["data"]
        assert len(data) == 1
        
        user = data[0]
        assert user["first_name"] == sample_user_data["first_name"]
        assert user["email"] == sample_user_data["email"]
        assert "face_embedding" not in user

    def test_list_users_multiple_users(self, client):
        """Test listing multiple registered users"""
        users_data = []
        for i in range(3):
            user_data = {
                "first_name": f"User{i}",
                "last_name": "Test",
                "email": f"user{i}@example.com",
                "age": 25 + i,
                "face_embedding": [0.1 * (i + 1)] * 128
            }
            users_data.append(user_data)
            client.post("/api/register", json=user_data)
        
        # List users
        response = client.get("/api/users")
        
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()["data"]
        assert len(data) == 3

    def test_list_users_no_embeddings(self, client, sample_user_data):
        """Test that list users response does not include embeddings"""
        # Register user
        client.post("/api/register", json=sample_user_data)
        
        # List users
        response = client.get("/api/users")
        
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()["data"]
        for user in data:
            assert "face_embedding" not in user

    def test_list_users_response_structure(self, client, sample_user_data):
        """Test list users response structure"""
        # Register user
        client.post("/api/register", json=sample_user_data)
        
        # List users
        response = client.get("/api/users")
        
        body = response.json()
        
        # Check top-level structure
        assert "success" in body
        assert "message" in body
        assert "data" in body
        
        # Check data is list
        assert isinstance(body["data"], list)
        
        # Check user structure in list
        if len(body["data"]) > 0:
            user = body["data"][0]
            required_fields = ["id", "first_name", "last_name", "email", "age"]
            for field in required_fields:
                assert field in user

    def test_list_users_includes_all_fields(self, client, sample_user_data):
        """Test that list users includes all required fields"""
        # Register user
        client.post("/api/register", json=sample_user_data)
        
        # List users
        response = client.get("/api/users")
        
        body = response.json()
        user = body["data"][0]
        
        # Should have all public fields
        assert "id" in user
        assert "first_name" in user
        assert "last_name" in user
        assert "email" in user
        assert "age" in user
        assert "created_at" in user
        
        # Values should match
        assert user["first_name"] == sample_user_data["first_name"]
        assert user["email"] == sample_user_data["email"]
