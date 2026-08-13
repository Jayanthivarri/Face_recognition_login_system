"""
User Schemas Module

Defines Pydantic models for request/response validation.
These schemas ensure type safety and automatic validation of all inputs.

Schemas:
    - UserCreate: Request schema for user registration
    - UserResponse: Response schema for user data
    - LoginRequest: Request schema for face login
    - LoginResponse: Response schema for login success

Features:
    - Automatic validation
    - Type checking
    - JSON schema generation
    - Swagger documentation
"""

from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, List
from datetime import datetime

class UserCreate(BaseModel):
    """
    Schema for user registration request.
    
    Attributes:
        first_name: User's first name (required, 2-100 chars)
        last_name: User's last name (required, 2-100 chars)
        email: User's email address (required, must be valid)
        age: User's age (optional, 18-120)
        face_embedding: 128-dimensional face descriptor (required)
    """
    
    first_name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="User's first name"
    )
    last_name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="User's last name"
    )
    email: EmailStr = Field(
        ...,
        description="User's email address"
    )
    age: Optional[int] = Field(
        None,
        ge=18,
        le=120,
        description="User's age (optional, 18-120)"
    )
    face_embedding: List[float] = Field(
        ...,
        description="128-dimensional face descriptor from FaceAPI.js"
    )
    
    @field_validator('face_embedding')
    @classmethod
    def validate_embedding(cls, v):
        """
        Validate face embedding.
        
        Checks:
            - Must be exactly 128 dimensions
            - All values must be valid floats
            - Values should be between -1 and 1
        """
        if len(v) != 128:
            raise ValueError(f"Face embedding must be 128-dimensional, got {len(v)}")
        
        # Ensure all values are float
        try:
            face_embedding = [float(x) for x in v]
        except (ValueError, TypeError):
            raise ValueError("All face embedding values must be numeric")
        
        # Validate range (typical face descriptors are normalized to [-1, 1])
        for i, val in enumerate(face_embedding):
            if val < -2 or val > 2:
                raise ValueError(f"Face embedding value at index {i} out of expected range [-2, 2]")
        
        return face_embedding
    
    class Config:
        json_schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "age": 30,
                "face_embedding": [0.1] * 128  # 128 values
            }
        }


class UserResponse(BaseModel):
    """
    Schema for user data in API responses.
    
    Attributes:
        id: User's unique identifier
        first_name: User's first name
        last_name: User's last name
        email: User's email address
        age: User's age
        created_at: Account creation timestamp
    
    Note:
        Face embedding is NOT included in responses for security
    """
    
    id: int
    first_name: str
    last_name: str
    email: str
    age: Optional[int] = None
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True  # Allow ORM model conversion
        json_schema_extra = {
            "example": {
                "id": 1,
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "age": 30,
                "created_at": "2024-01-15T10:30:00Z"
            }
        }


class LoginRequest(BaseModel):
    """
    Schema for face-based login request.
    
    Attributes:
        face_embedding: 128-dimensional face descriptor captured during login
    
    Usage:
        When user attempts to login via face recognition,
        their face embedding is extracted and sent to this endpoint
        for matching against stored embeddings.
    """
    
    face_embedding: List[float] = Field(
        ...,
        description="128-dimensional face descriptor from captured face"
    )
    
    @field_validator('face_embedding')
    @classmethod
    def validate_embedding(cls, v):
        """
        Validate face embedding for login.
    
        
        Same validation as UserCreate.face_embedding
        """
        if len(v) != 128:
            raise ValueError(f"Face embedding must be 128-dimensional, got {len(v)}")
        
        try:
            face_embedding = [float(x) for x in v]
        except (ValueError, TypeError):
            raise ValueError("All face embedding values must be numeric")
        
        for i, val in enumerate(face_embedding):
            if val < -2 or val > 2:
                raise ValueError(f"Face embedding value at index {i} out of expected range [-2, 2]")
        
        return face_embedding
    

    class Config:
        json_schema_extra = {
            "example": {
                "face_embedding": [0.1] * 128
            }
        }


class LoginResponse(BaseModel):
    """
    Schema for successful face login response.
    
    Attributes:
        success: Whether login was successful
        message: Response message
        user: Matched user information
        user_id: ID of matched user
    """
    
    success: bool
    message: str
    user: UserResponse
    user_id: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Login successful! Face matched.",
                "user": {
                    "id": 1,
                    "first_name": "John",
                    "last_name": "Doe",
                    "email": "john.doe@example.com",
                    "age": 30,
                    "created_at": "2024-01-15T10:30:00Z"
                },
                "user_id": 1
            }
        }


__all__ = [
    "UserCreate",
    "UserResponse",
    "LoginRequest",
    "LoginResponse"
]
