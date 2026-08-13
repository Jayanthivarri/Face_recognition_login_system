"""
Pytest Configuration and Fixtures

Provides shared fixtures and configuration for all tests.

Fixtures:
    - client: TestClient for API testing
    - test_db: In-memory test database
    - test_user: Sample user for testing
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.main import app
from app.database.base import Base
from app.database.session import get_db
from app.models.user import User

# ============================================================================
# Database Fixtures
# ============================================================================

# Create an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="function")
def test_db():
    """
    Create a test database for each test function.
    
    Uses an in-memory SQLite database that is created fresh for each test
    and destroyed after the test completes.
    
    Yields:
        Session: Database session for the test
    """
    # Create engine for in-memory SQLite
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
    )
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Create session factory
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
    
    # Override the get_db dependency
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    db = TestingSessionLocal()
    yield db
    
    db.close()
    
    # Drop all tables
    Base.metadata.drop_all(bind=engine)

# ============================================================================
# Client Fixtures
# ============================================================================

@pytest.fixture
def client(test_db):
    """
    Create a TestClient for API testing.
    
    Uses the test database fixture.
    
    Args:
        test_db: Test database fixture
    
    Returns:
        TestClient: FastAPI test client
    """
    return TestClient(app)

# ============================================================================
# Sample Data Fixtures
# ============================================================================

@pytest.fixture
def sample_user_data():
    """
    Provide sample user data for testing.
    
    Returns:
        dict: Sample user registration data
    """
    return {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "age": 30,
        "face_embedding": [0.1] * 128  # 128-dimensional embedding
    }

@pytest.fixture
def sample_face_embedding():
    """
    Provide a sample face embedding for testing.
    
    Returns:
        list: 128-dimensional face descriptor
    """
    return [0.1] * 128

@pytest.fixture
def sample_login_data(sample_face_embedding):
    """
    Provide sample login data for testing.
    
    Args:
        sample_face_embedding: Sample embedding fixture
    
    Returns:
        dict: Sample login request data
    """
    return {
        "face_embedding": sample_face_embedding
    }

# ============================================================================
# Pytest Hooks
# ============================================================================

def pytest_configure(config):
    """
    Configure pytest with custom settings.
    
    Called before test collection.
    """
    print("\n" + "="*70)
    print("  🧪 Test Configuration")
    print("="*70)
    print(f"  Database: In-memory SQLite")
    print(f"  Test discovery: tests/")
    print("="*70 + "\n")

def pytest_collection_modifyitems(config, items):
    """
    Modify test collection to add markers.
    
    Args:
        config: Pytest config
        items: Collected test items
    """
    # Mark all tests in tests/unit as unit tests
    for item in items:
        if "tests/unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        # Mark all tests in tests/integration as integration tests
        elif "tests/integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)

__all__ = [
    "test_db",
    "client",
    "sample_user_data",
    "sample_face_embedding",
    "sample_login_data"
]
