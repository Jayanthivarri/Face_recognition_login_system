# Backend Foundation Setup Guide

## 📋 Overview

This guide explains all the backend foundation files that have been generated and how they work together.

## 🗂️ File Structure

```
backend/
├── app/
│   ├── __init__.py                    # App package initialization
│   ├── main.py                        # FastAPI application setup
│   ├── database/
│   │   ├── __init__.py
│   │   ├── base.py                    # SQLAlchemy declarative base
│   │   ├── config.py                  # Database connection config
│   │   └── session.py                 # Session management
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py                    # User ORM model
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py                    # Pydantic models (requests/responses)
│   │   └── response.py                # Common response schemas
│   ├── services/
│   │   └── __init__.py                # Services placeholder
│   ├── routers/
│   │   └── __init__.py                # Routers placeholder
│   └── utils/
│       ├── __init__.py
│       ├── exceptions.py              # Custom exception classes
│       ├── validators.py              # Input validation functions
│       ├── helpers.py                 # Helper utilities
│       └── constants.py               # Application constants
├── tests/
│   ├── conftest.py                    # Pytest configuration and fixtures
│   ├── unit/                          # Unit tests
│   └── integration/                   # Integration tests
├── requirements.txt                   # Python dependencies
├── .env.example                       # Environment variables template
├── pytest.ini                         # Pytest configuration
├── run.py                             # Application entry point
└── README.md                          # Backend README
```

## 📦 Key Files Explained

### 1. **requirements.txt**
Contains all Python dependencies needed for the backend.

**Key Packages:**
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `sqlalchemy` - ORM
- `pydantic` - Data validation
- `numpy` - Numerical computing
- `pytest` - Testing framework

**Installation:**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

### 2. **app/main.py** - FastAPI Application
The main application setup file that:
- Creates the FastAPI app instance
- Configures CORS for frontend communication
- Sets up exception handlers
- Registers routes (when available)
- Initializes the database on startup
- Provides health check endpoint

**Key Features:**
```python
# CORS Configuration - allows frontend to communicate
app.add_middleware(CORSMiddleware, ...)

# Exception handling - consistent error responses
@app.exception_handler(AppException)
async def app_exception_handler(request, exc):
    ...

# Health check endpoint
@app.get("/api/health")
async def health_check():
    ...
```

**Start the app:**
```bash
python run.py
# or
uvicorn app.main:app --reload
```

The API will be available at: `http://localhost:8000`
- Swagger UI: `http://localhost:8000/api/docs`
- ReDoc: `http://localhost:8000/api/redoc`

### 3. **Database Configuration**

#### `app/database/base.py`
Provides the declarative base for all ORM models.
All models inherit from `Base` to be registered with the database.

```python
from app.database.base import Base

class User(Base):
    __tablename__ = "users"
    # columns...
```

#### `app/database/config.py`
Handles database connection and engine creation.

**Features:**
- Creates SQLAlchemy engine
- Configures connection pooling
- Handles different database types (SQLite, PostgreSQL, etc.)
- Echo SQL in debug mode

```python
from app.database.config import engine, DATABASE_URL

# The engine is automatically created
# DATABASE_URL read from environment or defaults to SQLite
```

#### `app/database/session.py`
Manages database sessions and provides dependency injection.

**Usage in endpoints:**
```python
from app.database.session import get_db
from sqlalchemy.orm import Session

@router.get("/items")
async def get_items(db: Session = Depends(get_db)):
    # db session is automatically provided and cleaned up
    return db.query(Item).all()
```

#### `app/database/__init__.py`
Exports all database utilities and provides `init_db()` function.

```python
from app.database import init_db

# Called on app startup to create tables
init_db()
```

### 4. **Models**

#### `app/models/user.py`
SQLAlchemy ORM model for the User table.

**Columns:**
- `id` - Primary key
- `first_name` - User's first name
- `last_name` - User's last name
- `email` - Unique email address
- `age` - Optional age
- `face_embedding` - 128D face descriptor stored as JSON
- `created_at` - Account creation timestamp

**Features:**
- Automatic timestamp generation
- JSON serialization support for embeddings
- String representation and conversion methods

### 5. **Schemas (Pydantic Models)**

#### `app/schemas/user.py`
Request/response validation models.

**Schemas:**
- **UserCreate** - Request for registration
  ```python
  {
      "first_name": "John",
      "last_name": "Doe",
      "email": "john@example.com",
      "age": 30,
      "face_embedding": [0.1, 0.2, ...]  # 128 values
  }
  ```

- **UserResponse** - Response with user data (no embedding)
  ```python
  {
      "id": 1,
      "first_name": "John",
      "last_name": "Doe",
      "email": "john@example.com",
      "age": 30,
      "created_at": "2024-01-15T10:30:00Z"
  }
  ```

- **LoginRequest** - Face embedding for login
  ```python
  {
      "face_embedding": [0.1, 0.2, ...]  # 128 values
  }
  ```

- **LoginResponse** - Successful login response
  ```python
  {
      "success": true,
      "message": "Login successful!",
      "user": {...},
      "user_id": 1
  }
  ```

**Validation Features:**
- Type checking
- Range validation (age 18-120)
- Embedding dimension validation (exactly 128)
- Email format validation
- Automatic error messages

#### `app/schemas/response.py`
Common response schemas for consistency.

**Schemas:**
- **ErrorResponse** - Standard error format
- **SuccessResponse** - Standard success format
- **ValidationErrorResponse** - Detailed validation errors

### 6. **Exception Handling**

#### `app/utils/exceptions.py`
Custom exception classes for application errors.

**Exceptions:**
- `AppException` - Base exception
- `ValidationException` - Input validation errors (422)
- `NotFoundError` - Resource not found (404)
- `DuplicateError` - Duplicate resource (409)
- `AuthenticationError` - Auth failures (401)
- `FaceMatchingError` - Face matching failures (400)

**Usage:**
```python
from app.utils.exceptions import DuplicateError, NotFoundError

# Raise exceptions
if user_exists:
    raise DuplicateError(
        message="Email already registered",
        field="email",
        value=email
    )

# These are automatically caught and converted to JSON responses
```

**Exception Handler in main.py:**
```python
@app.exception_handler(AppException)
async def app_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.message,
            "error_code": exc.error_code,
            "details": exc.details
        }
    )
```

### 7. **Validators**

#### `app/utils/validators.py`
Input validation functions.

**Functions:**
- `validate_email()` - Validate email format
- `validate_face_embedding()` - Validate embedding (128D, range -2 to 2)
- `validate_age()` - Validate age (18-120)
- `validate_name()` - Validate name field

### 8. **Helpers**

#### `app/utils/helpers.py`
Helper functions for common operations.

**Functions:**
- `format_error_response()` - Format errors consistently
- `format_success_response()` - Format success responses
- `PaginatedResponse` - Wrapper for paginated data
- `get_pagination_params()` - Validate pagination parameters

### 9. **Constants**

#### `app/utils/constants.py`
Application-wide constants.

**Constant Categories:**
- **Face Recognition:** `FACE_MATCH_THRESHOLD=0.6`, `FACE_EMBEDDING_DIMENSION=128`
- **User Constraints:** Name lengths, age ranges, email max length
- **API Messages:** Success and error messages
- **CORS:** Allowed origins and methods
- **Database:** Connection URL and pool settings
- **HTTP Status Codes:** For reference

**Usage:**
```python
from app.utils.constants import FACE_MATCH_THRESHOLD, MSG_LOGIN_SUCCESS

if distance < FACE_MATCH_THRESHOLD:
    return {"message": MSG_LOGIN_SUCCESS}
```

### 10. **Environment Configuration**

#### `.env.example`
Template for environment variables.

**Variables:**
```
# Database
DATABASE_URL=sqlite:///./face_recognition.db

# FastAPI
DEBUG=True
API_HOST=0.0.0.0
API_PORT=8000

# CORS
CORS_ORIGINS=["http://localhost:5173", "http://localhost:3000"]

# Face Recognition
FACE_MATCH_THRESHOLD=0.6
```

**To use:**
```bash
# Copy to .env
cp .env.example .env

# Set your values
# Then they'll be loaded by os.getenv()
```

### 11. **Testing Setup**

#### `pytest.ini`
Pytest configuration for test discovery and execution.

**Features:**
- Auto-discovers test files (`test_*.py`)
- Defines custom markers (unit, integration, async)
- Configures test paths
- Async test support

#### `tests/conftest.py`
Pytest fixtures and configuration.

**Fixtures:**
- `test_db` - In-memory test database
- `client` - FastAPI TestClient
- `sample_user_data` - Sample user for testing
- `sample_face_embedding` - Sample face embedding
- `sample_login_data` - Sample login data

**Run tests:**
```bash
# Run all tests
pytest

# Run only unit tests
pytest -m unit

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=app
```

### 12. **Entry Point**

#### `run.py`
Simple entry point to start the server.

```bash
python run.py
```

Features:
- Loads configuration from environment
- Displays startup information
- Handles graceful shutdown
- Auto-reload in debug mode

## 🚀 Quick Start

### 1. Setup Virtual Environment
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Create .env File
```bash
cp .env.example .env
```

### 4. Run the Server
```bash
python run.py
```

Server will start at: `http://localhost:8000`

### 5. Access API Documentation
- Swagger UI: `http://localhost:8000/api/docs`
- ReDoc: `http://localhost:8000/api/redoc`

## 📊 Architecture Flow

```
Request comes in
    ↓
CORS Middleware (checks allowed origins)
    ↓
Router handler (when available in Phase 3)
    ↓
Pydantic Schema validation (UserCreate, LoginRequest, etc.)
    ↓
Custom validators (validate_email, validate_embedding, etc.)
    ↓
Service layer (when available in Phase 3)
    ↓
Database session (via Depends(get_db))
    ↓
SQLAlchemy ORM operations
    ↓
Response schema (UserResponse, ErrorResponse, etc.)
    ↓
JSON response sent to client
    ↓
Exception caught → Exception handler → Error response
```

## 🧪 Testing

The test infrastructure is ready for Phase 3 when APIs are implemented.

**Test files will be created for:**
- Unit tests of individual functions
- Integration tests of API endpoints
- Face matching algorithm tests
- Database operation tests

**Example test structure:**
```python
@pytest.mark.unit
def test_validate_email(self):
    # Test individual validators
    assert validate_email("valid@email.com") == True

@pytest.mark.integration
async def test_register_endpoint(client, sample_user_data):
    # Test API endpoints with test client
    response = client.post("/api/register", json=sample_user_data)
    assert response.status_code == 201
```

## 📝 Next Steps (Phase 3)

The backend foundation is complete. Next phase will add:

1. **User Service** - User management business logic
2. **Face Matching Service** - Face recognition and embedding comparison
3. **Auth Router** - `/api/register` and `/api/login` endpoints
4. **Users Router** - `/api/users` and `/api/profile/{id}` endpoints
5. **API Tests** - Integration tests for all endpoints

All the infrastructure is in place and ready for Phase 3 implementation!

---

**Generated Files: 17**
- Database modules: 3
- Models: 1
- Schemas: 2
- Utils: 4
- Tests: 4
- App initialization: 1
- Config files: 2
