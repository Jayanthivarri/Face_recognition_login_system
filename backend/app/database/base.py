"""
Database Base Configuration Module

This module provides the declarative base for all SQLAlchemy models.
All ORM models should inherit from this Base class to be included
in database migrations and table creation.

Usage:
    from app.database.base import Base
    
    class User(Base):
        __tablename__ = "users"
        id = Column(Integer, primary_key=True)
"""

from sqlalchemy.orm import declarative_base

# Base class for all SQLAlchemy models
Base = declarative_base()

__all__ = ["Base"]
