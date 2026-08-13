"""
Database Configuration Module

This module handles all database connection and configuration settings.
It creates the SQLAlchemy engine and manages database connection strings.

Features:
    - SQLite database connection
    - Connection pooling
    - Echo configuration for debugging
    - Database URL management

Usage:
    from app.database.config import engine, DATABASE_URL
"""

from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from typing import Optional
import os
from pathlib import Path

# Get database URL from environment or use default
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./face_recognition.db")

# Get debug mode from environment
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

def get_database_url() -> str:
    """
    Get the database URL.
    
    Returns:
        str: The database connection URL
    """
    return DATABASE_URL

def create_database_engine():
    """
    Create and configure the SQLAlchemy engine.
    
    For SQLite:
        - Uses StaticPool for in-memory databases
        - Regular QueuePool for file-based databases
        - Echo SQL statements if DEBUG is True
    
    Returns:
        Engine: Configured SQLAlchemy engine
    """
    # Use StaticPool for SQLite in-memory databases
    # Use default QueuePool for file-based SQLite
    if "sqlite" in DATABASE_URL:
        # For SQLite, we need to handle threading
        engine = create_engine(
            DATABASE_URL,
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
            echo=DEBUG  # Print SQL statements if DEBUG is True
        )
    else:
        # For other databases (PostgreSQL, MySQL, etc.)
        engine = create_engine(
            DATABASE_URL,
            echo=DEBUG
        )
    
    return engine

# Create the engine instance
engine = create_database_engine()

__all__ = ["engine", "DATABASE_URL", "create_database_engine", "get_database_url"]
