# Backend - Face Recognition Login System

## 🚀 Quick Start

### 1. Setup Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Create Environment File
```bash
cp .env.example .env
```

### 4. Run Server
```bash
python run.py
```

Server starts at: **http://localhost:8000**

## 📚 Documentation

- **[PHASE_2_SUMMARY.md](PHASE_2_SUMMARY.md)** - Complete file-by-file explanation of all 24 files
- **[BACKEND_STRUCTURE.md](BACKEND_STRUCTURE.md)** - Folder structure and architecture overview
- **[docs/BACKEND_SETUP.md](docs/BACKEND_SETUP.md)** - Detailed setup guide

## 🏗️ Project Structure

```
app/
├── database/        # Database connection, sessions, models
├── models/          # SQLAlchemy ORM models
├── schemas/         # Pydantic request/response models
├── services/        # Business logic (Phase 3)
├── routers/         # API endpoints (Phase 3)
└── utils/           # Validators, exceptions, helpers, constants

tests/
├── unit/            # Unit tests
├── integration/     # Integration tests
└── conftest.py      # Pytest fixtures
```

## 🔌 API Endpoints

### Health Check
```bash
GET http://localhost:8000/api/health
```

### API Documentation
- **Swagger UI:** http://localhost:8000/api/docs
- **ReDoc:** http://localhost:8000/api/redoc

### Phase 3 Endpoints (Coming Soon)
- `POST /api/register` - User registration with face
- `POST /api/login` - Face-based login
- `GET /api/profile/{id}` - User profile
- `GET /api/users` - All users list

## 🧪 Testing

### Run All Tests
```bash
pytest
```

### Run Only Unit Tests
```bash
pytest -m unit
```

### Run Only Integration Tests
```bash
pytest -m integration
```

### Run with Verbose Output
```bash
pytest -v
```

### Run with Coverage
```bash
pytest --cov=app
```

## 📦 Technology Stack

- **FastAPI** 0.104.1 - Modern async web framework
- **SQLAlchemy** 2.0.23 - ORM for database
- **Pydantic** 2.5.0 - Data validation
- **SQLite** - Lightweight database
- **NumPy** 1.24.3 - Numerical computing
- **Pytest** 7.4.3 - Testing framework

## 🔐 Security

- **CORS** - Configured for frontend communication
- **Input Validation** - Pydantic schemas validate all inputs
- **Exception Handling** - No sensitive info leaked
- **SQL Injection Prevention** - SQLAlchemy parameterized queries
- **Face Embedding Only** - No images stored, only 128D vectors

## ⚙️ Configuration

### Environment Variables (.env)
```
DATABASE_URL=sqlite:///./face_recognition.db
DEBUG=True
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=["http://localhost:5173"]
FACE_MATCH_THRESHOLD=0.6
```

## 📊 Key Features

✅ **Database Setup**
- SQLite with SQLAlchemy ORM
- Automatic table creation on startup
- Session management with dependency injection

✅ **Data Validation**
- Pydantic schemas for request/response
- Custom validators for emails, embeddings, names
- Automatic API documentation

✅ **Exception Handling**
- Custom exception classes
- Automatic error response formatting
- Structured error messages

✅ **Testing Infrastructure**
- Pytest configuration
- Test fixtures for database and client
- Unit and integration test organization

✅ **API Documentation**
- Swagger UI (interactive)
- ReDoc (beautiful documentation)
- OpenAPI schema

## 🎯 Phase 2 Status: COMPLETE ✅

24 files generated with:
- FastAPI application setup
- Database configuration
- ORM models
- Pydantic schemas
- Exception handling
- Validation functions
- Test infrastructure

## 📋 Next Phase (Phase 3)

Phase 3 will implement:
- User registration API
- Face login API
- User profile API
- User listing API
- UserService layer
- FaceMatchingService layer
- Integration tests

## 💡 Development Tips

### Auto-reload During Development
The server auto-reloads when you change files if `DEBUG=True`.

### Inspect Database
```bash
# Connect to SQLite
sqlite3 face_recognition.db

# View tables
.tables

# View schema
.schema users
```

### Create New Models
1. Create model class in `app/models/`
2. Import in `app/models/__init__.py`
3. Restart server (tables auto-created)

### Add New Validators
1. Create function in `app/utils/validators.py`
2. Use in Pydantic schemas or services
3. Export in `app/utils/__init__.py`

### Add New Exception Types
1. Create class in `app/utils/exceptions.py`
2. Register in FastAPI exception handler if needed
3. Raise from services/routers

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Change port in .env
API_PORT=8001

# Or find process using port 8000
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows
```

### Database Locked
```bash
# SQLite is file-based, close all connections
# Delete the database file to reset
rm face_recognition.db

# Restart server to recreate
python run.py
```

### Pydantic Validation Error
Check the error message carefully - it will tell you:
- Which field has the error
- What the expected format is
- What you provided

## 📞 Support

For issues or questions, refer to:
- [PHASE_2_SUMMARY.md](PHASE_2_SUMMARY.md) - File documentation
- [docs/BACKEND_SETUP.md](docs/BACKEND_SETUP.md) - Setup guide
- FastAPI docs: https://fastapi.tiangolo.com
- SQLAlchemy docs: https://docs.sqlalchemy.org

---

**Current Phase:** 2 - Backend Foundation ✅
**Status:** Ready for Phase 3 APIs
**Generated:** 24 Files
**Total Code:** ~4,500 lines
