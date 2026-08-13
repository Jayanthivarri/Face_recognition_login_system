# 📚 Quick Reference Guide - Backend Foundation

## 🚀 Quick Start (2 minutes)

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

**API Available at:** http://localhost:8000/api/docs

---

## 📁 File Quick Reference

### Must-Know Files

| File | What It Does | When to Use |
|------|------------|-----------|
| `app/main.py` | FastAPI setup | Configuring app behavior |
| `app/models/user.py` | Database schema | Modifying user fields |
| `app/schemas/user.py` | Request validation | Changing API input/output |
| `app/utils/exceptions.py` | Error handling | Adding new error types |
| `app/utils/validators.py` | Input checks | Adding new validators |
| `tests/conftest.py` | Test setup | Writing new tests |

---

## 🗂️ Where Things Live

### I need to...

#### Add a new field to User table
**File:** `app/models/user.py`
```python
new_field = Column(String(100), nullable=True)
```

#### Change validation rules
**File:** `app/schemas/user.py`
```python
field_name = Field(..., min_length=X, max_length=Y)
```

#### Add a new error type
**File:** `app/utils/exceptions.py`
```python
class MyException(AppException):
    def __init__(self, message: str):
        super().__init__(
            message=message,
            error_code="MY_ERROR",
            status_code=400
        )
```

#### Add custom validation
**File:** `app/utils/validators.py`
```python
def validate_custom(value: str) -> bool:
    if not valid:
        raise ValidationException(...)
    return True
```

#### Create a new endpoint (Phase 3)
**File:** `app/routers/auth.py`
```python
from fastapi import APIRouter
router = APIRouter(prefix="/api")

@router.post("/my-endpoint")
async def my_endpoint(data: MySchema):
    return {"result": data}
```

#### Write a test
**File:** `tests/integration/test_api.py`
```python
def test_my_feature(client, sample_user_data):
    response = client.post("/api/register", json=sample_user_data)
    assert response.status_code == 201
```

---

## 🔍 Key Concepts

### Database Models (ORM)
```python
# Location: app/models/
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
```
**When to use:** Define database tables

### Schemas (Validation)
```python
# Location: app/schemas/
class UserCreate(BaseModel):
    email: EmailStr
    age: int = Field(..., ge=18, le=120)
```
**When to use:** Validate API requests/responses

### Exceptions
```python
# Location: app/utils/exceptions.py
raise DuplicateError(message="...", field="email")
```
**When to use:** Return errors to client

### Validators
```python
# Location: app/utils/validators.py
validate_email(email)
```
**When to use:** Custom validation logic

### Constants
```python
# Location: app/utils/constants.py
FACE_MATCH_THRESHOLD = 0.6
```
**When to use:** Configuration values

### Dependency Injection
```python
# Location: app/database/session.py
async def endpoint(db: Session = Depends(get_db)):
    users = db.query(User).all()
```
**When to use:** Access database in endpoints

---

## 📊 Common Tasks

### Task: Add new API endpoint

**Step 1:** Create router file `app/routers/my_router.py`
```python
from fastapi import APIRouter, Depends
from app.database.session import get_db

router = APIRouter(prefix="/api")

@router.post("/my-endpoint")
async def my_endpoint(data: MySchema, db: Session = Depends(get_db)):
    # Your code here
    return result
```

**Step 2:** Import in `app/main.py`
```python
from app.routers import my_router
app.include_router(my_router.router)
```

### Task: Add new database table

**Step 1:** Create model in `app/models/my_model.py`
```python
from app.database.base import Base

class MyModel(Base):
    __tablename__ = "my_table"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
```

**Step 2:** Import in `app/models/__init__.py`
```python
from app.models.my_model import MyModel
```

**Step 3:** Restart server (tables auto-created)

### Task: Add validation for a field

**Step 1:** Create validator in `app/utils/validators.py`
```python
def validate_my_field(value: str) -> bool:
    if not is_valid(value):
        raise ValidationException("Invalid value")
    return True
```

**Step 2:** Use in schema with `@field_validator`
```python
@field_validator('my_field')
def validate_field(cls, v):
    return validate_my_field(v)
```

### Task: Handle a new error type

**Step 1:** Create exception in `app/utils/exceptions.py`
```python
class MyException(AppException):
    def __init__(self, message: str):
        super().__init__(message, error_code="MY_ERROR", status_code=400)
```

**Step 2:** Raise it in your code
```python
raise MyException("Something went wrong")
```

**Step 3:** It's automatically caught and formatted!

---

## 🧪 Testing Quick Reference

### Run all tests
```bash
pytest
```

### Run specific test file
```bash
pytest tests/unit/test_validators.py
```

### Run specific test
```bash
pytest tests/unit/test_validators.py::test_validate_email
```

### Run with verbose output
```bash
pytest -v
```

### Run only unit tests
```bash
pytest -m unit
```

### Run only integration tests
```bash
pytest -m integration
```

### Run with coverage
```bash
pytest --cov=app
```

### View available markers
```bash
pytest --markers
```

---

## 🔗 Import Cheat Sheet

### Database
```python
from app.database import init_db, get_db, SessionLocal, Base
from app.database.session import get_db
```

### Models
```python
from app.models import User
from app.models.user import User
```

### Schemas
```python
from app.schemas import UserCreate, UserResponse, ErrorResponse
from app.schemas.user import UserCreate
```

### Exceptions
```python
from app.utils import ValidationException, DuplicateError
from app.utils.exceptions import AppException
```

### Validators
```python
from app.utils import validate_email, validate_face_embedding
from app.utils.validators import validate_email
```

### Helpers
```python
from app.utils import format_error_response, format_success_response
from app.utils.helpers import PaginatedResponse
```

### Constants
```python
from app.utils.constants import FACE_MATCH_THRESHOLD, MSG_LOGIN_SUCCESS
from app.utils import constants
```

---

## 🐛 Common Issues & Solutions

### Issue: `ModuleNotFoundError: No module named 'app'`
**Solution:** 
- Make sure you're in the `backend/` directory
- Make sure `app/` folder exists
- Check Python path includes current directory

### Issue: Database is locked
**Solution:**
- Close all database connections
- Delete `face_recognition.db` to reset
- Restart the server

### Issue: Port 8000 already in use
**Solution:**
- Change port in `.env`: `API_PORT=8001`
- Or kill process: `lsof -i :8000` (macOS/Linux)

### Issue: Validation error on startup
**Solution:**
- Check `.env` file exists and is readable
- Verify all required environment variables are set
- Look for typos in configuration values

### Issue: `CORS error` in frontend
**Solution:**
- Check `CORS_ORIGINS` in `.env` includes frontend URL
- Make sure you're using correct origin format
- Restart backend after changing CORS settings

---

## 📝 Environment Variables

```
# .env file
DATABASE_URL=sqlite:///./face_recognition.db  # Database path
DEBUG=True                                      # Debug mode
API_HOST=0.0.0.0                              # Server host
API_PORT=8000                                 # Server port
CORS_ORIGINS=["http://localhost:5173"]        # Allowed frontend
FACE_MATCH_THRESHOLD=0.6                      # Face matching threshold
```

---

## 🎯 API Response Examples

### Success Response
```json
{
  "success": true,
  "message": "Operation successful",
  "data": {...},
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Error Response
```json
{
  "success": false,
  "message": "Email already registered",
  "error_code": "DUPLICATE_EMAIL",
  "details": {"field": "email"},
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Validation Error Response
```json
{
  "success": false,
  "message": "Validation failed",
  "error_code": "VALIDATION_ERROR",
  "validation_errors": [
    {
      "field": "email",
      "message": "Invalid email format",
      "value": "invalid"
    }
  ],
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

## 📚 Key Files Relationship

```
Request comes in
    ↓
main.py (CORS middleware)
    ↓
Router in routers/ (Phase 3)
    ↓
Schema validates (schemas/)
    ↓
Custom validators (utils/validators.py)
    ↓
Service processes (services/ - Phase 3)
    ↓
Database query (models/ + database/)
    ↓
Response formatted (schemas/ or utils/helpers.py)
    ↓
JSON sent to client
```

---

## ✨ Phase 3 Preview

What will be added:

### New Files (Phase 3)
- `app/routers/auth.py` - Registration & login
- `app/routers/users.py` - Profile & user list
- `app/services/user_service.py` - User operations
- `app/services/face_matching_service.py` - Face recognition

### New Endpoints
- `POST /api/register` - Register with face
- `POST /api/login` - Login with face
- `GET /api/profile/{id}` - Get profile
- `GET /api/users` - List users

---

## 🔗 Useful Links

- **FastAPI Docs:** https://fastapi.tiangolo.com
- **SQLAlchemy Docs:** https://docs.sqlalchemy.org
- **Pydantic Docs:** https://docs.pydantic.dev
- **Pytest Docs:** https://docs.pytest.org
- **HTTP Status Codes:** https://httpwg.org/specs/rfc7231.html#status.codes

---

## 📞 Quick Help

**Need to understand a file?**
1. Read docstring at top of file
2. Check `PHASE_2_SUMMARY.md` in backend directory
3. Read `docs/BACKEND_SETUP.md` for detailed explanation

**Need to start the server?**
```bash
python run.py
```

**Need to run tests?**
```bash
pytest -v
```

**Need API documentation?**
Visit: http://localhost:8000/api/docs

---

**Current Phase:** 2 - Backend Foundation ✅
**Total Files:** 24
**Ready for:** Phase 3 Backend APIs
