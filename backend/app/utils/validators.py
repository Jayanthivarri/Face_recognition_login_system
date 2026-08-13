"""
Validators Module

Provides validation functions for common operations.
These validators ensure data integrity throughout the application.

Functions:
    - validate_email: Validate email format and availability
    - validate_face_embedding: Validate face embedding structure
    - validate_age: Validate age value
"""

import re
from typing import List
from app.utils.exceptions import ValidationException

def validate_email(email: str) -> bool:
    """
    Validate email format.
    
    Checks:
        - Valid email format
        - Reasonable length
    
    Args:
        email: Email address to validate
    
    Returns:
        bool: True if valid
    
    Raises:
        ValidationException: If email is invalid
    """
    # Simple email validation regex
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not email:
        raise ValidationException(
            message="Email cannot be empty",
            details={"field": "email"}
        )
    
    if len(email) > 255:
        raise ValidationException(
            message="Email is too long (max 255 characters)",
            details={"field": "email", "length": len(email)}
        )
    
    if not re.match(email_pattern, email):
        raise ValidationException(
            message="Invalid email format",
            details={"field": "email", "value": email}
        )
    
    return True


def validate_face_embedding(embedding: List[float]) -> bool:
    """
    Validate face embedding format and values.
    
    Checks:
        - Must be list of floats
        - Must be exactly 128 dimensions
        - Values must be in valid range
    
    Args:
        embedding: Face embedding to validate
    
    Returns:
        bool: True if valid
    
    Raises:
        ValidationException: If embedding is invalid
    """
    # Check if it's a list
    if not isinstance(embedding, list):
        raise ValidationException(
            message="Face embedding must be a list",
            details={"field": "face_embedding", "type": type(embedding).__name__}
        )
    
    # Check length
    if len(embedding) != 128:
        raise ValidationException(
            message=f"Face embedding must be 128-dimensional, got {len(embedding)}",
            details={"field": "face_embedding", "dimensions": len(embedding)}
        )
    
    # Validate each value
    try:
        for i, val in enumerate(embedding):
            if not isinstance(val, (int, float)):
                raise ValueError(f"Value at index {i} is not numeric")
            
            # Check range (face descriptors are typically normalized)
            if val < -2 or val > 2:
                raise ValueError(f"Value at index {i} is out of expected range [-2, 2]")
    
    except ValueError as e:
        raise ValidationException(
            message=f"Invalid face embedding: {str(e)}",
            details={"field": "face_embedding"}
        )
    
    return True


def validate_age(age: int) -> bool:
    """
    Validate age value.
    
    Checks:
        - Must be integer
        - Must be in reasonable range (18-120)
    
    Args:
        age: Age to validate
    
    Returns:
        bool: True if valid
    
    Raises:
        ValidationException: If age is invalid
    """
    if not isinstance(age, int):
        raise ValidationException(
            message="Age must be an integer",
            details={"field": "age", "type": type(age).__name__}
        )
    
    if age < 18 or age > 120:
        raise ValidationException(
            message="Age must be between 18 and 120",
            details={"field": "age", "value": age}
        )
    
    return True


def validate_name(name: str, field_name: str = "name") -> bool:
    """
    Validate name field.
    
    Checks:
        - Not empty
        - Reasonable length (2-100 chars)
        - Contains only allowed characters
    
    Args:
        name: Name to validate
        field_name: Field name for error messages
    
    Returns:
        bool: True if valid
    
    Raises:
        ValidationException: If name is invalid
    """
    if not name or not isinstance(name, str):
        raise ValidationException(
            message=f"{field_name.title()} cannot be empty",
            details={"field": field_name}
        )
    
    # Check length
    if len(name) < 2 or len(name) > 100:
        raise ValidationException(
            message=f"{field_name.title()} must be between 2 and 100 characters",
            details={"field": field_name, "length": len(name)}
        )
    
    # Check for valid characters (letters, spaces, hyphens)
    name_pattern = r'^[a-zA-Z\s\-\']{2,100}$'
    if not re.match(name_pattern, name):
        raise ValidationException(
            message=f"{field_name.title()} contains invalid characters",
            details={"field": field_name, "value": name}
        )
    
    return True


__all__ = [
    "validate_email",
    "validate_face_embedding",
    "validate_age",
    "validate_name"
]
