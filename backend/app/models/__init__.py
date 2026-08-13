"""
Models Module

Exports all SQLAlchemy ORM models for the application.
These models are automatically registered with the database Base
and are used for table creation and data operations.

Exports:
    - User: User model with face embeddings
"""

from app.models.user import User

__all__ = ["User"]
