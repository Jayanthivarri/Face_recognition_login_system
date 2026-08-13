"""
User Routes - API endpoints for user management
Implements registration, login, and profile endpoints
"""

import logging
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.user import UserCreate, UserResponse, LoginRequest, LoginResponse
from app.schemas.response import ErrorResponse, SuccessResponse
from app.services.user_service import UserService
from app.services.face_matching_service import FaceMatchingService
from app.utils.exceptions import (
    ValidationException,
    NotFoundError,
    DuplicateError,
    AuthenticationError,
    FaceMatchingError
)
from app.utils.constants import MSG_REGISTRATION_SUCCESS, MSG_LOGIN_SUCCESS, MSG_USER_NOT_FOUND

logger = logging.getLogger(__name__)

# Create router for user endpoints
router = APIRouter(prefix="/api", tags=["users"])


@router.post(
    "/register",
    response_model=SuccessResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register new user with face",
    description="Register a new user with face embedding for face recognition login"
)
async def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new user with face embedding.
    
    ## Request Body
    - **first_name**: User's first name (2-100 characters)
    - **last_name**: User's last name (2-100 characters)
    - **email**: User's email (unique)
    - **age**: User's age (18-120, optional)
    - **face_embedding**: Face embedding vector (exactly 128 floats, range -2 to 2)
    
    ## Response
    - **success**: true if registration successful
    - **message**: Success message
    - **data**: Created user data (id, names, email, created_at)
    
    ## Error Codes
    - 422: Validation error in request data
    - 409: Email already registered
    - 500: Server error
    """
    try:
        logger.info(f"Registration attempt for email: {user_data.email}")
        
        # Create user using service
        db_user = UserService.create_user(db, user_data)
        
        logger.info(f"User registered successfully: {db_user.id}")
        
        # Return success response
        return SuccessResponse(
            success=True,
            message=MSG_REGISTRATION_SUCCESS,
            data={
                "id": db_user.id,
                "first_name": db_user.first_name,
                "last_name": db_user.last_name,
                "email": db_user.email,
                "age": db_user.age,
                "created_at": db_user.created_at.isoformat() if db_user.created_at else None
            }
        )
        
    except DuplicateError as e:
        logger.warning(f"Duplicate email registration: {user_data.email}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"error": e.message, "error_code": e.error_code}
        )
    except ValidationException as e:
        logger.warning(f"Validation error during registration: {e.message}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"error": e.message, "error_code": e.error_code}
        )
    except Exception as e:
        logger.error(f"Unexpected error during registration: {str(e)}")
        print("ACTUAL REGISTRATION ERROR:", repr(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Registration failed", "error_code": "REGISTRATION_FAILED"}
        )


@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    summary="Login with face embedding",
    description="Login by matching face embedding against registered users using Euclidean distance"
)
async def login_user(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Login using face embedding.
    
    Matches provided face embedding against all registered users using
    Euclidean distance. Returns matched user if distance is below threshold.
    
    ## Request Body
    - **face_embedding**: Face embedding vector (exactly 128 floats, range -2 to 2)
    
    ## Response
    - **success**: true if login successful
    - **message**: Success message
    - **user**: Matched user data
    - **user_id**: ID of matched user
    - **confidence**: Confidence score (0-1) of the match
    - **distance**: Euclidean distance to matched user
    
    ## Error Codes
    - 422: Validation error in request data
    - 401: Face not recognized - no match found
    - 500: Server error
    """
    try:
        logger.info("Login attempt with face embedding")
        
        # Get all users with embeddings
        users_with_embeddings = UserService.get_users_with_embeddings(db)
        
        if not users_with_embeddings:
            logger.warning("No registered users found for login")
            raise AuthenticationError(
                message="No registered users found",
                error_code="NO_USERS_REGISTERED"
            )
        
        # Find nearest match using face matching service
        match_result = FaceMatchingService.find_nearest_match(
            query_embedding=login_data.face_embedding,
            database_embeddings=users_with_embeddings
        )
        
        if match_result is None:
            logger.warning("Face recognition failed - no match found")
            raise AuthenticationError(
                message="Face not recognized",
                error_code="FACE_NOT_RECOGNIZED"
            )
        
        matched_user_id, distance = match_result
        
        # Get full user details
        matched_user = UserService.get_user_by_id(db, matched_user_id)
        
        # Calculate confidence score
        confidence = FaceMatchingService.get_match_confidence(distance)
        print("==========")
        print("MATCHED USER:", matched_user_id)
        print("DISTANCE:", distance)
        print("CONFIDENCE:", confidence)
        print("==========")
        logger.info(
            f"Login successful: user_id={matched_user_id}, "
            f"distance={distance:.4f}, confidence={confidence:.2%}"
        )
        
        # Return login response
        return LoginResponse(
            success=True,
            message=MSG_LOGIN_SUCCESS,
            user={
                "id": matched_user.id,
                "first_name": matched_user.first_name,
                "last_name": matched_user.last_name,
                "email": matched_user.email,
                "age": matched_user.age
            },
            user_id=matched_user.id,
            confidence=confidence,
            distance=round(distance, 4)
        )
        
    except AuthenticationError as e:
        logger.warning(f"Authentication failed: {e.message}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": e.message, "error_code": e.error_code}
        )
    except FaceMatchingError as e:
        logger.error(f"Face matching error: {e.message}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": e.message, "error_code": e.error_code}
        )
    except ValidationException as e:
        logger.warning(f"Validation error during login: {e.message}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"error": e.message, "error_code": e.error_code}
        )
    except Exception as e:
        logger.error(f"Unexpected error during login: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Login failed", "error_code": "LOGIN_FAILED"}
        )


@router.get(
    "/profile/{user_id}",
    response_model=SuccessResponse,
    status_code=status.HTTP_200_OK,
    summary="Get user profile",
    description="Retrieve user profile information by user ID"
)
async def get_user_profile(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Get user profile information.
    
    Retrieves user's public profile information (without face embedding).
    
    ## Path Parameters
    - **user_id**: User ID
    
    ## Response
    - **success**: true if retrieval successful
    - **message**: Success message
    - **data**: User profile (id, first_name, last_name, email, age, created_at)
    
    ## Error Codes
    - 404: User not found
    - 500: Server error
    """
    try:
        logger.info(f"Profile retrieval for user: {user_id}")
        
        # Get user profile
        profile = UserService.get_user_profile(db, user_id)
        
        if profile is None:
            logger.warning(f"User not found: {user_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "error": MSG_USER_NOT_FOUND,
                    "error_code": "USER_NOT_FOUND"
                }
            )
        
        logger.info(f"Profile retrieved successfully: {user_id}")
        
        # Return success response
        return SuccessResponse(
            success=True,
            message="Profile retrieved successfully",
            data=profile
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error retrieving profile for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Profile retrieval failed", "error_code": "PROFILE_RETRIEVAL_FAILED"}
        )


@router.get(
    "/users",
    response_model=SuccessResponse,
    status_code=status.HTTP_200_OK,
    summary="List all registered users",
    description="Retrieve list of all registered users (without face embeddings)"
)
async def list_users(
    db: Session = Depends(get_db)
):
    """
    List all registered users.
    
    Returns list of all users without face embeddings.
    
    ## Response
    - **success**: true if retrieval successful
    - **message**: Success message
    - **data**: List of user profiles
    
    ## Error Codes
    - 500: Server error
    """
    try:
        logger.info("Listing all users")
        
        # Get all users
        users = UserService.get_all_users(db)
        
        # Convert to dictionaries without embeddings
        users_data = [
            {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "age": user.age,
                "created_at": user.created_at.isoformat() if user.created_at else None
            }
            for user in users
        ]
        
        logger.info(f"Retrieved {len(users_data)} users")
        
        # Return success response
        return SuccessResponse(
            success=True,
            message=f"Found {len(users_data)} users",
            data=users_data
        )
        
    except Exception as e:
        logger.error(f"Error listing users: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Failed to retrieve users", "error_code": "LIST_USERS_FAILED"}
        )
