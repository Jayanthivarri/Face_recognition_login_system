# Face Recognition Login System

## About the Project

This project is a face recognition-based login system that allows users to register and log in using their face instead of a password.

I built the frontend using React and TypeScript, and the backend using FastAPI and Python. The application uses FaceAPI.js to detect faces and generate 128-dimensional face embeddings. During login, the captured embedding is compared with registered embeddings using Euclidean distance to identify the user.

## Features

- User registration with personal details and face capture
- Real-time face detection through a webcam
- Passwordless login using facial recognition
- Face matching using Euclidean distance
- Rejection of unregistered faces
- Dashboard to view registered users
- SQLite database for storing user details and face embeddings

## Tech Stack

**Frontend:** React, TypeScript, Vite, FaceAPI.js, CSS

**Backend:** Python, FastAPI, SQLAlchemy, Pydantic, NumPy

**Database:** SQLite

## How It Works

1. A new user enters their details and captures their face during registration.
2. The system generates a 128-dimensional face embedding and stores it with the user's information.
3. During login, a new face embedding is generated from the webcam.
4. The backend compares it with registered embeddings using Euclidean distance.
5. If a suitable match is found within the configured threshold, the user is logged in. Otherwise, access is denied.

## Project Structure

```text
Face_recognition_login_system/
├── frontend/
├── backend/
├── docs/
├── README.md
├── PROJECT_STRUCTURE.md
└── ARCHITECTURE_DIAGRAM.md
```

## How to Run

### Backend

```bash
cd backend
python -m venv venv
```

Activate the virtual environment.

**Windows:**
```bash
venv\Scripts\activate
```

Install dependencies and start the server:

```bash
pip install -r requirements.txt
python run.py
```

Backend: `http://localhost:8000`

API documentation: `http://localhost:8000/api/docs`

### Frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the local URL shown in the terminal, usually `http://localhost:5173`.

Allow camera access when prompted by the browser.

## Project Resources

- **GitHub:** https://github.com/Jayanthivarri/Face_recognition_login_system
- **Architecture:** `ARCHITECTURE_DIAGRAM.md`
- **Project Structure:** `PROJECT_STRUCTURE.md`
- **Backend Setup:** `docs/BACKEND_SETUP.md`

## Future Improvements

Possible improvements include liveness detection, protection against photo-based spoofing, and additional authentication methods.

## Author

Varri Jayanthi