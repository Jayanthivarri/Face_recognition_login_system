"""
Registration API Tests

Tests for user registration endpoint (POST /api/register)
"""

import pytest
from fastapi import status
from sqlalchemy.orm import Session

from app.models.user import User


class TestRegistration:
    """Tests for registration endpoint"""

    def test_register_user_success(self, client, sample_user_data):
        """Test successful user registration"""
        response = client.post("/api/register", json=sample_user_data)
        
        # Check response status
        assert response.status_code == status.HTTP_201_CREATED
        
        # Check response structure
        assert response.json()["success"] is True
        assert "message" in response.json()
        assert "data" in response.json()
        
        # Check user data in response
        data = response.json()["data"]
        assert data["first_name"] == sample_user_data["first_name"]
        assert data["last_name"] == sample_user_data["last_name"]
        assert data["email"] == sample_user_data["email"]
        assert data["age"] == sample_user_data["age"]
        assert "id" in data
        assert "created_at" in data

    def test_register_user_duplicate_email(self, client, sample_user_data, test_db):
        """Test registration with duplicate email"""
        # Register first user
        response1 = client.post("/api/register", json=sample_user_data)
        assert response1.status_code == status.HTTP_201_CREATED
        
        # Try to register with same email
        response2 = client.post("/api/register", json=sample_user_data)
        
        # Check error response
        assert response2.status_code == status.HTTP_409_CONFLICT
        assert response2.json()["success"] is False
        assert "error_code" in response2.json()

    def test_register_user_missing_first_name(self, client, sample_user_data):
        """Test registration with missing first name"""
        data = sample_user_data.copy()
        del data["first_name"]
        
        response = client.post("/api/register", json=data)
        
        # Should fail validation
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_register_user_missing_last_name(self, client, sample_user_data):
        """Test registration with missing last name"""
        data = sample_user_data.copy()
        del data["last_name"]
        
        response = client.post("/api/register", json=data)
        
        # Should fail validation
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_register_user_missing_email(self, client, sample_user_data):
        """Test registration with missing email"""
        data = sample_user_data.copy()
        del data["email"]
        
        response = client.post("/api/register", json=data)
        
        # Should fail validation
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_register_user_missing_embedding(self, client, sample_user_data):
        """Test registration with missing face embedding"""
        data = sample_user_data.copy()
        del data["face_embedding"]
        
        response = client.post("/api/register", json=data)
        
        # Should fail validation
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_register_user_invalid_email(self, client, sample_user_data):
        """Test registration with invalid email"""
        data = sample_user_data.copy()
        data["email"] = "invalid_email"
        
        response = client.post("/api/register", json=data)
        
        # Should fail validation
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_register_user_invalid_embedding_dimension(self, client, sample_user_data):
        """Test registration with wrong embedding dimension"""
        data = sample_user_data.copy()
        # Create embedding with wrong dimension (127 instead of 128)
        data["face_embedding"] = [0.1] * 127
        
        response = client.post("/api/register", json=data)
        
        # Should fail validation
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_register_user_embedding_values_out_of_range(self, client, sample_user_data):
        """Test registration with embedding values outside range"""
        data = sample_user_data.copy()
        # Create embedding with values outside [-2, 2]
        data["face_embedding"] = [5.0] * 128
        
        response = client.post("/api/register", json=data)
        
        # Should fail validation
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_register_user_invalid_age(self, client, sample_user_data):
        """Test registration with invalid age"""
        data = sample_user_data.copy()
        # Age below minimum (18)
        data["age"] = 15
        
        response = client.post("/api/register", json=data)
        
        # Should fail validation
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_register_user_age_above_max(self, client, sample_user_data):
        """Test registration with age above maximum"""
        data = sample_user_data.copy()
        # Age above maximum (120)
        data["age"] = 150
        
        response = client.post("/api/register", json=data)
        
        # Should fail validation
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_register_user_short_first_name(self, client, sample_user_data):
        """Test registration with first name too short"""
        data = sample_user_data.copy()
        # Name with only 1 character
        data["first_name"] = "A"
        
        response = client.post("/api/register", json=data)
        
        # Should fail validation
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_register_user_stored_in_database(self, client, sample_user_data, test_db):
        """Test that registered user is actually stored in database"""
        response = client.post("/api/register", json=sample_user_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        user_id = response.json()["data"]["id"]
        
        # Query database to verify
        user = test_db.query(User).filter(User.id == user_id).first()
        assert user is not None
        assert user.first_name == sample_user_data["first_name"]
        assert user.email == sample_user_data["email"]

    def test_register_multiple_users(self, client):
        """Test registering multiple different users"""
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
        
        assert response1.status_code == status.HTTP_201_CREATED
        assert response2.status_code == status.HTTP_201_CREATED
        
        # IDs should be different
        id1 = response1.json()["data"]["id"]
        id2 = response2.json()["data"]["id"]
        assert id1 != id2

    def test_register_response_format(self, client, sample_user_data):
        """Test that response format matches specification"""
        response = client.post("/api/register", json=sample_user_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        
        body = response.json()
        
        # Check top-level structure
        assert "success" in body
        assert "message" in body
        assert "data" in body
        
        # Check success value
        assert body["success"] is True
        
        # Check data structure
        data = body["data"]
        required_fields = ["id", "first_name", "last_name", "email", "age", "created_at"]
        for field in required_fields:
            assert field in data
        
        # Make sure face_embedding is NOT included in response
        assert "face_embedding" not in data
