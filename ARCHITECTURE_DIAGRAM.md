# Architecture Diagram - Face Recognition Login System

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT SIDE (React + Vite)               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    Application Shell                      │   │
│  │  (App.tsx - Routing, Auth Context, Global State)         │   │
│  └──────────────────────────────────────────────────────────┘   │
│                              │                                   │
│   ┌──────────────┬───────────┼───────────┬──────────────┐       │
│   │              │           │           │              │       │
│   ▼              ▼           ▼           ▼              ▼       │
│ ┌─────┐    ┌────────┐    ┌─────┐    ┌────────┐    ┌────────┐  │
│ │Login│    │Register│    │Profile│   │Layout │    │Navbar  │  │
│ │Page │    │Page    │    │Page  │   │       │    │        │  │
│ └─────┘    └────────┘    └─────┘    └────────┘    └────────┘  │
│   │            │            │                                    │
│   └────────┬───┴────────┬───┘                                    │
│            │            │                                        │
│   ┌────────▼─────┐  ┌───▼────────────┐                         │
│   │  Components  │  │  Protected     │                         │
│   │  Layer       │  │  Routes        │                         │
│   └──────────────┘  └────────────────┘                         │
│   │                                                              │
│   │ • CameraPreview                                             │
│   │ • FaceCapture                                               │
│   │ • FormField                                                 │
│   │ • Button, Card, Loader                                      │
│   │                                                              │
│   └─────────────────┬──────────────────────────────────────┐   │
│                     │                                       │   │
│   ┌─────────────────▼──────────────────┐                  │   │
│   │      Custom Hooks Layer            │                  │   │
│   ├────────────────────────────────────┤                  │   │
│   │ • useCamera (webcam access)        │                  │   │
│   │ • useFaceDetection (FaceAPI.js)    │                  │   │
│   │ • useAuth (auth state)             │                  │   │
│   │ • useLocalStorage (persistence)    │                  │   │
│   └──────────────┬─────────────────────┘                  │   │
│                  │                                         │   │
│   ┌──────────────▼──────────────────────┐                │   │
│   │    Services Layer (API Client)      │                │   │
│   ├──────────────────────────────────────┤                │   │
│   │ • authService (register, login)     │                │   │
│   │ • faceService (face processing)     │                │   │
│   │ • userService (profile, list users) │                │   │
│   │ • api.ts (Axios instance)           │                │   │
│   └──────────────┬──────────────────────┘                │   │
│                  │                                        │   │
│   ┌──────────────▼─────────────────────────┐            │   │
│   │    Face Recognition Engine            │            │   │
│   ├────────────────────────────────────────┤            │   │
│   │ • FaceAPI.js Models                   │            │   │
│   │   - TinyFaceDetector                  │            │   │
│   │   - FaceLandmark68Net                 │            │   │
│   │   - FaceRecognitionNet                │            │   │
│   │                                        │            │   │
│   │ • Processing Pipeline                 │            │   │
│   │   1. detectSingleFace()               │            │   │
│   │   2. withFaceLandmarks()              │            │   │
│   │   3. withFaceDescriptor()             │            │   │
│   │                                        │            │   │
│   │ • Output: 128D Embedding              │            │   │
│   └────────────────┬─────────────────────┘            │   │
│                    │                                    │   │
│                    └────────────┐                       │   │
│                                 │                       │   │
└─────────────────────────────────┼───────────────────────┘   │
                                  │                             │
                    HTTP/CORS (Axios)                          │
                                  │                             │
┌─────────────────────────────────▼─────────────────────────┐  │
│                  BACKEND API (FastAPI)                     │  │
├──────────────────────────────────────────────────────────┤  │
│                                                            │  │
│  ┌────────────────────────────────────────────────────┐   │  │
│  │           FastAPI Application (main.py)           │   │  │
│  │  • CORS Configuration                             │   │  │
│  │  • Exception Handlers                             │   │  │
│  │  • Middleware Setup                               │   │  │
│  └────────────────────────────────────────────────────┘   │  │
│                        │                                   │  │
│     ┌──────────────────┼──────────────────┐               │  │
│     │                  │                  │               │  │
│     ▼                  ▼                  ▼               │  │
│  ┌─────────┐      ┌──────────┐      ┌──────────┐        │  │
│  │Auth     │      │Users     │      │Health    │        │  │
│  │Router   │      │Router    │      │Router    │        │  │
│  └─────────┘      └──────────┘      └──────────┘        │  │
│     │                  │                  │               │  │
│     │  POST /register  │  GET /users     │  GET /health  │  │
│     │  POST /login     │  GET /profile   │                │  │
│     │                  │                  │               │  │
│     └──────────────────┼──────────────────┘               │  │
│                        │                                   │  │
│     ┌──────────────────▼──────────────────┐               │  │
│     │    Validation Layer (Pydantic)      │               │  │
│     ├───────────────────────────────────────┤             │  │
│     │ • UserRegister Schema                │             │  │
│     │ • UserLogin Schema                   │             │  │
│     │ • Response Schemas                   │             │  │
│     └──────────────────┬──────────────────┘               │  │
│                        │                                   │  │
│     ┌──────────────────▼──────────────────┐               │  │
│     │    Services Layer                    │               │  │
│     ├───────────────────────────────────────┤             │  │
│     │ • UserService                        │               │  │
│     │   - create_user()                    │               │  │
│     │   - get_user_by_id()                 │               │  │
│     │   - get_all_users()                  │               │  │
│     │                                       │               │  │
│     │ • FaceMatchingService                │               │  │
│     │   - match_face(embedding)            │               │  │
│     │   - calculate_euclidean_distance()   │               │  │
│     │   - find_closest_match()             │               │  │
│     │   - threshold = 0.6                  │               │  │
│     │                                       │               │  │
│     │ • EmbeddingService                   │               │  │
│     │   - validate_embedding()             │               │  │
│     │   - parse_embedding()                │               │  │
│     └──────────────────┬──────────────────┘               │  │
│                        │                                   │  │
│     ┌──────────────────▼──────────────────┐               │  │
│     │    Database Layer                    │               │  │
│     ├───────────────────────────────────────┤             │  │
│     │ • SQLAlchemy ORM                     │               │  │
│     │ • Session Management                 │               │  │
│     │ • Connection Pooling                 │               │  │
│     │ • Dependency Injection               │               │  │
│     └──────────────────┬──────────────────┘               │  │
│                        │                                   │  │
└────────────────────────┼───────────────────────────────────┘  │
                         │                                       │
                    SQLite Protocol                              │
                         │                                       │
┌────────────────────────▼───────────────────────────────────┐   │
│             DATABASE (SQLite)                              │   │
├────────────────────────────────────────────────────────────┤   │
│                                                            │   │
│  ┌──────────────────────────────────────────────────────┐ │   │
│  │  Table: users                                        │ │   │
│  ├────────────────────────────────────────────────────────┤│   │
│  │ • id (INTEGER PRIMARY KEY)                           ││   │
│  │ • first_name (VARCHAR)                               ││   │
│  │ • last_name (VARCHAR)                                ││   │
│  │ • email (VARCHAR UNIQUE)                             ││   │
│  │ • age (INTEGER)                                      ││   │
│  │ • face_embedding (JSON) - 128D vector               ││   │
│  │ • created_at (TIMESTAMP)                             ││   │
│  └──────────────────────────────────────────────────────┘ │   │
│                                                            │   │
└────────────────────────────────────────────────────────────┘   │
```

## Data Flow Diagrams

### Registration Flow
```
User Input
    │
    ▼
┌──────────────────┐
│  Form Validation │
└────────┬─────────┘
         │
         ▼
┌──────────────────────┐
│  Open Webcam         │
│  (useCamera hook)    │
└────────┬─────────────┘
         │
         ▼
┌──────────────────────┐
│  Capture Face        │
│  (useFaceDetection)  │
└────────┬─────────────┘
         │
         ▼
┌──────────────────────────────┐
│  Generate 128D Embedding     │
│  (FaceAPI.js)                │
│  - detectSingleFace()        │
│  - withFaceLandmarks()       │
│  - withFaceDescriptor()      │
└────────┬─────────────────────┘
         │
         ▼
┌──────────────────────────────┐
│  POST /api/register          │
│  (authService)               │
│  Body: {user_data, embedding}│
└────────┬─────────────────────┘
         │ (HTTP)
         ▼
┌──────────────────────────────┐
│  Validate Input              │
│  (Pydantic Schema)           │
└────────┬─────────────────────┘
         │
         ▼
┌──────────────────────────────┐
│  Store in Database           │
│  (SQLAlchemy Model)          │
└────────┬─────────────────────┘
         │
         ▼
┌──────────────────────────────┐
│  Return User ID + Token      │
│  (Response Schema)           │
└────────┬─────────────────────┘
         │
         ▼
Redirect to Login
```

### Login & Face Matching Flow
```
Open Webcam
    │
    ▼
┌──────────────────────┐
│  Capture Face        │
│  (useFaceDetection)  │
└────────┬─────────────┘
         │
         ▼
┌──────────────────────────────┐
│  Generate 128D Embedding     │
│  (FaceAPI.js)                │
└────────┬─────────────────────┘
         │
         ▼
┌──────────────────────────────┐
│  POST /api/login             │
│  (authService)               │
│  Body: {embedding}           │
└────────┬─────────────────────┘
         │ (HTTP)
         ▼
┌──────────────────────────────┐
│  Face Matching Service       │
│  ├─ Load all users from DB   │
│  ├─ Parse embeddings         │
│  └─ Calculate distances      │
└────────┬─────────────────────┘
         │
         ▼
┌──────────────────────────────┐
│  Euclidean Distance Check    │
│  for each user:              │
│  distance = √Σ(x-y)²        │
└────────┬─────────────────────┘
         │
         ▼
┌──────────────────────────────┐
│  Compare with Threshold      │
│  if distance < 0.6:          │
│    ✓ Match Found             │
│  else:                       │
│    ✗ No Match                │
└────────┬─────────────────────┘
         │
    ┌────┴────┐
    │          │
    ▼          ▼
 Match     No Match
    │          │
    ▼          ▼
Return User  Return Error
Profile      Message
    │          │
    ▼          ▼
Redirect    Show Error
to Profile  on Login
```

## Component Hierarchy

```
App
├── Router
│   ├── ProtectedRoute
│   │   └── Profile
│   ├── Login
│   └── Register
│
└── Common Components
    ├── Navbar
    ├── Button
    ├── Card
    ├── Loading
    ├── Notification
    └── ErrorBoundary

Auth Components
├── CameraPreview
│   ├── Video Element
│   ├── Canvas Element
│   └── Capture Button
├── FaceCapture
│   ├── Detection Status
│   ├── Retry Button
│   └── Confirm Button
└── FormField
    ├── Input
    ├── Label
    └── Error Message
```

## Service Layer Architecture

```
Services
│
├── api.ts (Axios Configuration)
│   ├── Base URL
│   ├── Default Headers
│   ├── Request Interceptors
│   └── Response Interceptors
│
├── authService.ts
│   ├── register(userData, embedding)
│   └── login(embedding)
│
├── faceService.ts
│   ├── loadFaceModels()
│   ├── detectFace(canvas)
│   ├── generateEmbedding(canvas)
│   └── validateDetection(detection)
│
└── userService.ts
    ├── getUserProfile(id)
    ├── getAllUsers()
    └── updateProfile(id, data)
```

## State Management Flow

```
Local Component State (React Hooks)
│
├── User Data (useAuth)
│   ├── userId
│   ├── userProfile
│   └── isAuthenticated
│
├── Camera State (useCamera)
│   ├── isCameraOpen
│   ├── constraints
│   └── stream
│
├── Face Detection State (useFaceDetection)
│   ├── isDetecting
│   ├── detectedFaces
│   └── embedding
│
└── UI State (Components)
    ├── Loading States
    ├── Error Messages
    └── Notification States

LocalStorage (useLocalStorage)
│
├── Auth Token
├── User ID
├── Refresh Token
└── User Preferences
```

## API Endpoint Structure

```
POST /api/register
├── Request Body
│   ├── first_name: string
│   ├── last_name: string
│   ├── email: string
│   ├── age: number
│   └── face_embedding: array[128]
└── Response
    ├── user_id: integer
    ├── message: string
    └── token: string

POST /api/login
├── Request Body
│   └── face_embedding: array[128]
└── Response
    ├── user_id: integer
    ├── first_name: string
    ├── last_name: string
    ├── email: string
    ├── age: number
    └── token: string

GET /api/profile/{user_id}
├── Response
│   ├── user_id: integer
│   ├── first_name: string
│   ├── last_name: string
│   ├── email: string
│   └── age: number

GET /api/users
├── Response
│   └── users: array[
│       ├── user_id
│       ├── first_name
│       ├── last_name
│       └── email
│   ]
```

## Technology Stack Integration

```
Frontend Layer
├── React 18+ (UI)
├── Vite (Build Tool)
├── TypeScript (Type Safety)
├── Axios (HTTP Client)
└── React Router DOM (Routing)

Face Recognition Layer
├── FaceAPI.js (Detection & Embedding)
├── TensorFlow.js (Model Execution)
└── Canvas API (Image Processing)

Backend Layer
├── FastAPI (Web Framework)
├── Python 3.9+ (Runtime)
├── Pydantic (Validation)
└── SQLAlchemy (ORM)

Database Layer
├── SQLite (Database)
├── numpy (Numerical Computing)
└── numpy.linalg (Distance Calculations)
```

## Security Architecture

```
Client-Side Security
├── Input Validation
├── Face Embedding Only (No Images Sent)
├── LocalStorage Encryption (Token)
└── Protected Routes

Server-Side Security
├── Pydantic Validation
├── CORS Configuration
├── SQL Injection Prevention (SQLAlchemy)
├── Error Handling (No Sensitive Info)
└── Distance Threshold (0.6)
```
